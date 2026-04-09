import time
import random
import csv
import json
import django
import resend
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ChangePasswordForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.apps import apps


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request=request)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                request.session.pop('verification_code', None)
                request.session.pop('verification_code_time', None)
                return redirect('home')
            except IntegrityError:
                form.add_error(None, "Une erreur est survenue : cet utilisateur existe probablement déjà.")
    else:
        form = CustomUserCreationForm(request=request)
    
    return render(request, 'connexion/inscription.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        if u_name:
            u_name = u_name.strip().lower() 

        from django.db.models import Q
        from .models import User
        
        user_obj = User.objects.filter(Q(username=u_name) | Q(email=u_name)).first()

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=p_word)
        else:
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            if not user_obj:
                messages.error(request, "Ce compte n'existe pas.")
            else:
                messages.error(request, "Mot de passe incorrect.")
    
    return render(request, 'connexion/connexion.html')

def home(request):
    # logout(request)
    return render(request, 'accueil.html')

ALLOWED_AVATARS = [
    'person', 'person_2', 'person_3', 'person_4',
    'face', 'face_2', 'face_3', 'face_4', 'face_5', 'face_6',
    'mood', 'sentiment_satisfied', 'emoji_emotions',
    'school', 'psychology', 'medical_services',
    'science', 'biotech', 'health_and_safety',
    'stethoscope', 'vaccines', 'medication',
    'star', 'favorite', 'diamond',
]

@login_required
def account(request):
    """Redirige vers le bon dashboard selon le rôle de l'utilisateur."""
    user = request.user
    password_changed = False

    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                for error in e.messages:
                    form.add_error('new_password', error)
            
            if not form.errors:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Mot de passe modifié avec succès.")
                password_changed = True
                form = ChangePasswordForm(user)
    else:
        form = ChangePasswordForm(user)

    return render(request, 'account_settings.html', {
        'form': form,
        'allowed_avatars': ALLOWED_AVATARS,
        'password_changed': password_changed,
    })

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def change_avatar(request):
    if request.method == 'POST':
        avatar = request.POST.get('avatar', '').strip()
        if avatar in ALLOWED_AVATARS:
            request.user.avatar = avatar
            request.user.save(update_fields=['avatar'])
            return JsonResponse({'status': 'ok', 'avatar': avatar})
        return JsonResponse({'status': 'error', 'message': 'Avatar invalide.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required
def student_dashboard(request):
    from .models import StudentPerformance
    from django.db.models import Avg, Max, Min, Count
    import statistics as stats_lib

    last_trainings = StudentPerformance.objects.filter(
        student__user=request.user, is_finished=True
    ).select_related('case').order_by('-realization_date')[:3] # je ne sais pas 2 ou 3 comme vous voudrais

    finished_qs = StudentPerformance.objects.filter(
        student__user=request.user, is_finished=True
    )

    total_cases_done = finished_qs.count()

    scored_qs = finished_qs.exclude(total_score=None)
    agg = scored_qs.aggregate(
        avg_score=Avg('total_score'),
        max_score=Max('total_score'),
        min_score=Min('total_score'),
    )
    avg_score = round(agg['avg_score'], 1) if agg['avg_score'] is not None else None
    max_score = agg['max_score']
    min_score = agg['min_score']

    scores_list = list(scored_qs.values_list('total_score', flat=True))
    median_score = round(stats_lib.median(scores_list), 1) if scores_list else None

    if scores_list and max_score is not None:
        threshold = 50 if max_score > 20 else 10
        nb_success = sum(1 for s in scores_list if s >= threshold)
        success_rate = round((nb_success / len(scores_list)) * 100) if scores_list else 0
    else:
        success_rate = None

    best_performance = scored_qs.order_by('-total_score').select_related('case').first()

    context = {
        'last_trainings': last_trainings,
        'total_cases_done': total_cases_done,
        'avg_score': avg_score,
        'max_score': max_score,
        'min_score': min_score,
        'median_score': median_score,
        'success_rate': success_rate,
        'best_performance': best_performance,
    }
    return render(request, 'dashboard.html', context)

@login_required
def student_trainings(request):
    from .models import StudentPerformance
    trainings = StudentPerformance.objects.filter(
        student__user=request.user
    ).select_related('case').order_by('-realization_date')
    return render(request, 'case/student_trainings.html', {'trainings': trainings})

@login_required
def teacher_dashboard(request):
    from .models import ClinicalCase, Training, StudentPerformance, Professor
    from django.db.models import Avg, Count

    try:
        professor = request.user.professor_profile
    except Exception:
        professor = None

    # Derniers cas créés par ce professeur
    recent_cases = []
    total_cases_created = 0
    total_trainings = 0
    total_students_followed = 0
    recent_performances = []

    if professor:
        cases_qs = ClinicalCase.objects.filter(creator_professor=professor).order_by('-created_at')
        total_cases_created = cases_qs.count()
        recent_cases = list(cases_qs[:5])

        # Entraînements de ce professeur
        trainings_qs = Training.objects.filter(professor=professor).select_related('case', 'group')
        total_trainings = trainings_qs.count()

        # Étudiants suivis (via groupes liés aux entraînements)
        from .models import Student
        total_students_followed = Student.objects.filter(
            groups__professors=professor
        ).distinct().count()

        # Dernières performances sur les cas de ce professeur
        recent_performances = StudentPerformance.objects.filter(
            case__creator_professor=professor,
            is_finished=True
        ).select_related('case', 'student__user').order_by('-realization_date')[:8]

    context = {
        'recent_cases': recent_cases,
        'total_cases_created': total_cases_created,
        'total_trainings': total_trainings,
        'total_students_followed': total_students_followed,
        'recent_performances': recent_performances,
    }
    return render(request, 'dashboard.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    from .models import User, Student, Professor, Ticket, ClinicalCase, Training
    from django.utils import timezone
    from datetime import timedelta
    total_users = User.objects.get_all().count()
    total_students = User.objects.get_by_role('student').count()
    total_teachers = User.objects.get_by_role('teacher').count()
    total_admins = User.objects.filter(is_superuser=True).count() + User.objects.filter(role='admin').count()
    verified_emails = User.objects.get_verified().count()
    users_with_a2f = User.objects.get_with_a2f_enabled().count()
    total_tickets = Ticket.objects.all().count()
    open_tickets = Ticket.objects.get_by_status('Ouvert').count()
    in_progress_tickets = Ticket.objects.get_by_status('En cours').count()
    resolved_tickets = Ticket.objects.get_by_status('Clos').count()
    total_cases = ClinicalCase.objects.all().count()
    total_trainings = Training.objects.all().count()
    finished_trainings = Training.objects.get_finished_trainings().count()
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_registrations = User.objects.filter(date_joined__gte=seven_days_ago).count()
    latest_users = User.objects.all().order_by('-date_joined')[:10].values(
        'id', 'username', 'first_name', 'last_name', 'role', 'date_joined'
    )
    latest_tickets = Ticket.objects.all().order_by('-created_at')[:10].values(
        'id', 'subject', 'status', 'created_at', 'user__username'
    )

    # Construire les logs combinés
    logs = []
    for u in latest_users:
        logs.append({
            'type': 'registration',
            'icon': 'person_add',
            'message': f"{u['first_name']} {u['last_name']} ({u['username']})",
            'detail': u['role'] or 'student',
            'date': u['date_joined'],
        })
    for t in latest_tickets:
        logs.append({
            'type': 'ticket',
            'icon': 'confirmation_number',
            'message': t['subject'],
            'detail': t['status'],
            'date': t['created_at'],
            'user': t['user__username'],
        })
    # Trier par date décroissante
    logs.sort(key=lambda x: x['date'], reverse=True)
    logs = logs[:15]

    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_admins': total_admins,
        'verified_emails': verified_emails,
        'users_with_a2f': users_with_a2f,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'resolved_tickets': resolved_tickets,
        'total_cases': total_cases,
        'total_trainings': total_trainings,
        'finished_trainings': finished_trainings,
        'recent_registrations': recent_registrations,
        'logs': logs,
    }

    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def users(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    from .models import Student, Professor, Group
    from django.db.models import Q

    search_query = request.GET.get('search', '').strip()
    selected_university = request.GET.get('university', '')
    selected_professor_id = request.GET.get('professor_id', '')
    
    # 1. Obtenir toutes les universités distinctes
    prof_univs = Professor.objects.exclude(university='').values_list('university', flat=True)
    student_univs = Student.objects.exclude(university='').values_list('university', flat=True)
    all_universities = sorted(list(set(list(prof_univs) + list(student_univs))))
    
    professors = []
    students = []
    selected_professor = None
    search_professors = []
    search_students = []

    # 2. Recherche globale par nom / prénom
    if search_query:
        search_professors = Professor.objects.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).select_related('user')

        search_students = Student.objects.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).select_related('user')

    elif selected_university:
        # 3. Professeurs de l'université
        professors = Professor.objects.filter(university=selected_university).select_related('user')
        
        # 4. Si un professeur est sélectionné
        if selected_professor_id:
            try:
                selected_professor = Professor.objects.get(id=int(selected_professor_id))
                # Étudiants affiliés à ce prof via le modèle Group
                students = Student.objects.filter(
                    groups__professors=selected_professor
                ).distinct().select_related('user')
            except (ValueError, Professor.DoesNotExist):
                selected_professor_id = ''

    context = {
        'universities': all_universities,
        'selected_university': selected_university,
        'professors': professors,
        'selected_professor_id': int(selected_professor_id) if selected_professor_id else '',
        'selected_professor': selected_professor,
        'students': students,
        'search_query': search_query,
        'search_professors': search_professors,
        'search_students': search_students,
    }
    return render(request, 'administrater/users.html', context)

def logs(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    from .models import User, Ticket, StudentPerformance
    from django.utils import timezone
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)

    latest_users = User.objects.filter(date_joined__gte=thirty_days_ago).order_by('-date_joined').values(
        'id', 'username', 'first_name', 'last_name', 'role', 'date_joined'
    )
    latest_tickets = Ticket.objects.filter(created_at__gte=thirty_days_ago).order_by('-created_at').values(
        'id', 'subject', 'status', 'created_at', 'user__username'
    )
    latest_performances = StudentPerformance.objects.filter(realization_date__gte=thirty_days_ago).order_by('-realization_date').values(
        'id', 'student__user__username', 'case__name', 'realization_date', 'total_score'
    )
    
    logs = []
    for users in latest_users:
        logs.append({
            'type': 'registration',
            'icon': 'person_add',
            'message': f"Inscription : {users['first_name']} {users['last_name']} ({users['username']})",
            'detail': users['role'] or 'student',
            'date': users['date_joined'],
        })
    for tickets in latest_tickets:
        logs.append({
            'type': 'ticket',
            'icon': 'confirmation_number',
            'message': f"Ticket ({tickets['user__username']}) : {tickets['subject']}",
            'detail': tickets['status'],
            'date': tickets['created_at'],
        })
    for performances in latest_performances:
        logs.append({
            'type': 'performance',
            'icon': 'psychology',
            'message': f"Entraînement : {performances['student__user__username']} sur le cas {performances['case__name']}",
            'detail': f"Score: {performances['total_score']}" if performances['total_score'] is not None else "En cours",
            'date': performances['realization_date'],
        })
        
    logs.sort(key=lambda x: x['date'], reverse=True)
    logs = logs[:100]
    
    return render(request, 'administrater/logs.html', {'logs': logs})

def data(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Champs exportables pour les étudiants à voir avec le laboratoire
    student_fields = [
        ('user__first_name', 'Prénom'),
        ('user__last_name', 'Nom'),
        ('user__email', 'Email'),
        ('user__username', "Nom d'utilisateur"),
        ('ine', 'INE'),
        ('age', 'Âge'),
        ('gender', 'Genre'),
        ('degree_level', 'Niveau de diplôme'),
        ('year_of_study', "Année d'étude"),
        ('speciality', 'Spécialité'),
        ('university', 'Université'),
        ('rgpd_consent', 'Consentement RGPD'),
        ('scientific_study', 'Consentement étude scientifique'),
    ]

    # Champs exportables pour les enseignants à voir avec le laboratoire
    teacher_fields = [
        ('user__first_name', 'Prénom'),
        ('user__last_name', 'Nom'),
        ('user__email', 'Email'),
        ('user__username', "Nom d'utilisateur"),
        ('speciality', 'Spécialité'),
        ('university', 'Université'),
        ('rgpd_consent', 'Consentement RGPD'),
    ]

    # Champs exportables pour les performances
    performance_fields = [
        ('id', 'ID Performance'),
        ('realization_date', 'Date de réalisation'),
        ('student__ine', 'INE Étudiant'),
        ('case__name', 'Cas Clinique'),
        ('total_score', 'Note totale'),
        ('clinical_skills_score', 'Notes compétences cliniques'),
        ('communication_skills_score', 'Notes communication'),
        ('completion_time', 'Temps de réalisation'),
        ('is_finished', 'Terminé'),
    ]

    context = {
        'student_fields': student_fields,
        'teacher_fields': teacher_fields,
        'performance_fields': performance_fields,
    }

    return render(request, 'administrater/data-export.html', context)

def send_code_view(request):
    email = request.GET.get('email', '').strip().lower()
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email manquant'})

    # Initialiser la clé à chaque appel (en cas de rechargement du .env)
    resend.api_key = settings.RESEND_API_KEY

    if not resend.api_key:
        return JsonResponse({'status': 'error', 'message': 'Clé API Resend non configurée dans le .env'})

    code = str(random.randint(100000, 999999))
    request.session['verification_code'] = code
    request.session['verification_code_time'] = time.time()

    try:
        resend.Emails.send({
            "from": "mail@mailentreprise.carodavid2026.fr",
            "to": [email],
            "subject": "Votre code de vérification — DR. VIRTUORL",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto; padding: 32px;
                            border: 1px solid #e5e7eb; border-radius: 12px;">
                    <h2 style="color: #111827; margin-bottom: 8px;">Vérification de votre adresse email</h2>
                    <p style="color: #6b7280; margin-bottom: 24px;">
                        Utilisez le code ci-dessous pour finaliser votre inscription sur <strong>DR. VIRTUORL</strong>.
                        Ce code est valable <strong>10 minutes</strong>.
                    </p>
                    <div style="background: #f3f4f6; border-radius: 8px; padding: 24px; text-align: center;">
                        <span style="font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #111827;">
                            {code}
                        </span>
                    </div>
                    <p style="color: #9ca3af; font-size: 12px; margin-top: 24px;">
                        Si vous n'avez pas demandé ce code, ignorez cet email.
                    </p>
                </div>
            """,
        })
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def verify_code(request):
    code_saisi = request.GET.get('code', '').strip()
    code_attendu = request.session.get('verification_code')
    code_timestamp = request.session.get('verification_code_time', 0)
    
    if not code_attendu:
        return JsonResponse({'status': 'error', 'message': "Aucun code envoyé. Veuillez cliquer sur \"Envoyer le code\" d'abord."})
        
    if time.time() - code_timestamp > 600:
        return JsonResponse({'status': 'error', 'message': "Le code a expiré. Veuillez en demander un nouveau."})
        
    if code_saisi != code_attendu:
        return JsonResponse({'status': 'error', 'message': "Code de vérification incorrect."})
        
    return JsonResponse({'status': 'ok'})

@login_required
def export_students_csv(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="etudiants.csv"'
    response.write('\ufeff')
    writer = csv.writer(response, delimiter=';')
    
    writer.writerow([
        'Prénom', 'Nom', 'Email', "Nom d'utilisateur",
        'INE', 'Âge', 'Genre', 'Niveau de diplôme',
        "Année d'étude", 'Spécialité', 'Université',
        'Consentement RGPD', 'Consentement étude scientifique'
    ])
    
    from .models import Student
    students = Student.objects.select_related('user').all()
    for student in students:
        writer.writerow([
            student.user.first_name,
            student.user.last_name,
            student.user.email,
            student.user.username,
            student.ine,
            student.age,
            student.gender,
            student.degree_level,
            student.year_of_study,
            student.speciality,
            student.university,
            'Oui' if student.rgpd_consent else 'Non',
            'Oui' if student.scientific_study else 'Non'
        ])
        
    return response

def set_language(request, lang):
    if lang in ['fr', 'en']:
        request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def legal_notices(request):
    return render(request, 'infos/mentions_legales.html')

def privacy_policies(request):
    return render(request, 'infos/politiques_confidentialite.html')

@login_required
def open_ticket(request):
    return render(request, 'infos/ouvrir_ticket.html')

@login_required
def contact(request):
    if request.method == 'POST':
        sujet = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        if sujet and message:
            from .models import Ticket
            Ticket.objects.create(
                user=request.user,
                subject=sujet,
                message=message,
                status='Ouvert'
            )
            

            try:
                if resend.api_key:
                    resend.Emails.send({
                        "from": "mail@mailentreprise.carodavid2026.fr",
                        "to": [request.user.email],
                        "subject": "Confirmation de création de ticket — DR. VIRTUORL",
                        "html": f"""
                            <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto; padding: 32px; border: 1px solid #e5e7eb; border-radius: 12px;">
                                <h2 style="color: #111827; margin-bottom: 8px;">Votre ticket a bien été créé</h2>
                                <p style="color: #6b7280; margin-bottom: 24px;">Bonjour {request.user.first_name},</p>
                                <p style="color: #6b7280; margin-bottom: 24px;">
                                    Nous avons bien reçu votre demande concernant le sujet suivant : <strong>{sujet}</strong>.
                                    <br>
                                    {message}
                                </p>
                                <p style="color: #6b7280; margin-bottom: 24px;">
                                    Notre équipe va le traiter dans les plus brefs délais. Vous pouvez suivre l'état de votre ticket depuis votre tableau de bord.
                                </p>
                                <p style="color: #6b7280; margin-bottom: 24px;">
                                    Cordialement,
                                    <br>
                                    L'équipe DR. VIRTUORL
                                </p>
                            </div>
                        """,
                    })
            except Exception as e:
                pass
                
            messages.success(request, "Votre ticket a bien été créé. Vous allez recevoir un email de confirmation.")
            return redirect('ticket')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'infos/contact.html')

@login_required
def ticket(request):
    from .models import Ticket
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'infos/dashboard_ticket.html', {'tickets': tickets})

def study_details(request):
    return render(request, 'infos/details_etude.html')

def ticket_admin(request):
    if not request.user.is_superuser:
        return redirect('home')
    from .models import Ticket

    status = request.GET.get('status', '').strip()
    subject = request.GET.get('subject', '').strip()
    username = request.GET.get('user', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    zero_replies = request.GET.get('zero_replies', '').strip() == 'true'

    tickets = Ticket.objects.search(
        subject=subject or None,
        status=status or None,
        username=username or None,
        date_from=date_from or None,
        date_to=date_to or None,
        zero_replies=zero_replies
    ).order_by('-created_at')

    context = {
        'tickets': tickets,
        'ticket_count': tickets.count(),
        'filter_status': status,
        'filter_subject': subject,
        'filter_user': username,
        'filter_date_from': date_from,
        'filter_date_to': date_to,
        'filter_zero_replies': 'true' if zero_replies else '',
        'status_choices': ['Ouvert', 'En cours', 'Résolu', 'Clos'],
    }

    return render(request, 'administrater/ticket_admin.html', context)

@login_required
def ticket_detail(request, ticket_id):
    from .models import Ticket, TicketReply
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check permissions
    if not request.user.is_superuser and ticket.user != request.user:
        messages.error(request, "Accès refusé.")
        return redirect('home')
        
    if request.method == 'POST':
        message = request.POST.get('reply_message', '').strip()
        if message and ticket.status.lower() != 'clos':
            reply = TicketReply.objects.create(
                ticket=ticket,
                user=request.user,
                message=message
            )
            # Envoyer un e-mail à l'auteur si la réponse vient de l'administrateur
            if request.user.is_superuser:
                try:
                    import resend
                    if resend.api_key:
                        resend.Emails.send({
                            "from": "mail@mailentreprise.carodavid2026.fr",
                            "to": [ticket.user.email],
                            "subject": f"Nouvelle réponse à votre ticket #{ticket.id} — DR. VIRTUORL",
                            "html": f"""
                                <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto; padding: 32px; border: 1px solid #e5e7eb; border-radius: 12px;">
                                    <h2 style="color: #111827; margin-bottom: 8px;">Nouvelle réponse sur votre ticket</h2>
                                    <p style="color: #6b7280; margin-bottom: 24px;">Bonjour {ticket.user.first_name},</p>
                                    <p style="color: #6b7280; margin-bottom: 24px;">
                                        Une nouvelle réponse a été apportée à votre ticket concernant : <strong>{ticket.subject}</strong>.<br><br>
                                        <strong>Statut actuel du ticket :</strong> {ticket.status}
                                    </p>
                                    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #5ba2cf; margin-bottom: 24px;">
                                        <p style="margin: 0; color: #333;"><strong>Dernier message :</strong></p>
                                        <p style="margin-top: 5px; color: #555;">{message}</p>
                                    </div>
                                    <p style="color: #6b7280; margin-bottom: 24px;">
                                        Vous pouvez consulter la discussion complète depuis votre tableau de bord.
                                    </p>
                                </div>
                            """,
                        })
                except Exception as e:
                    pass
            messages.success(request, "Votre réponse a été ajoutée.")
            return redirect('ticket_detail', ticket_id=ticket.id)
            
    replies = ticket.replies.all()
    return render(request, 'infos/ticket_detail.html', {'ticket': ticket, 'replies': replies})

@login_required
def ticket_change_status(request, ticket_id):
    if not request.user.is_superuser:
        return redirect('home')
        
    if request.method == 'POST':
        from .models import Ticket
        ticket = get_object_or_404(Ticket, id=ticket_id)
        new_status = request.POST.get('status')
        if new_status in ['Ouvert', 'En cours', 'Résolu', 'Clos']:
            ticket.status = new_status
            ticket.save()
            messages.success(request, f"Le statut du ticket a été mis à jour sur '{new_status}'.")
            
    return redirect('ticket_detail', ticket_id=ticket_id)

@login_required
def all_cases(request):
    from .models import ClinicalCase

    name = request.GET.get('name', '').strip()
    speciality = request.GET.get('speciality', '').strip()
    study_level = request.GET.get('study_level', '').strip()
    knowledge_level = request.GET.get('knowledge_level', '').strip()
    primary_learning_domain = request.GET.get('primary_learning_domain', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    cases = ClinicalCase.objects.search(
        name=name or None,
        speciality=speciality or None,
        study_level=study_level or None,
        knowledge_level=knowledge_level or None,
        primary_learning_domain=primary_learning_domain or None,
        date_from=date_from or None,
        date_to=date_to or None,
    ).order_by('-created_at')

    # création dynamique des filtres, pas en dur donc on peut rajouter des spécialités
    all_specialities = sorted(ClinicalCase.objects.exclude(speciality='').values_list('speciality', flat=True).distinct())
    all_study_levels = sorted(ClinicalCase.objects.exclude(study_level='').values_list('study_level', flat=True).distinct())
    all_knowledge_levels = sorted(ClinicalCase.objects.exclude(knowledge_level='').values_list('knowledge_level', flat=True).distinct())
    all_domains = sorted(ClinicalCase.objects.exclude(primary_learning_domain='').values_list('primary_learning_domain', flat=True).distinct())

    context = {
        'cases': cases,
        'case_count': cases.count(),
        'filter_name': name,
        'filter_speciality': speciality,
        'filter_study_level': study_level,
        'filter_knowledge_level': knowledge_level,
        'filter_primary_learning_domain': primary_learning_domain,
        'filter_date_from': date_from,
        'filter_date_to': date_to,
        'speciality_choices': all_specialities,
        'study_level_choices': all_study_levels,
        'knowledge_level_choices': all_knowledge_levels,
        'domain_choices': all_domains,
    }
    return render(request, 'case/all_case.html', context)

@login_required
def random_case(request):
    from .models import ClinicalCase
    case_obj = ClinicalCase.objects.order_by('?').first()
    if case_obj:
        return redirect('case_detail', case_id=case_obj.id)
    return redirect('all_cases')

@login_required
def case_detail(request, case_id):
    from .models import ClinicalCase
    case_obj = get_object_or_404(ClinicalCase, id=case_id)
    return render(request, 'case/case_detail.html', {'case': case_obj})

@login_required
def start_case(request, case_id):
    if request.method != 'POST':
        return redirect('case_detail', case_id=case_id)
        
    from .models import ClinicalCase, Student, StudentPerformance
    from django.utils import timezone
    from django.contrib import messages
    
    case_obj = get_object_or_404(ClinicalCase, id=case_id)
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Seuls les étudiants peuvent démarrer un cas.")
        return redirect('case_detail', case_id=case_id)
        
    # Création de l'essai (StudentPerformance)
    performance = StudentPerformance.objects.create(
        student=student,
        case=case_obj,
        realization_date=timezone.now()
    )
    
    return redirect('play_performance', performance_id=performance.id)

@login_required
def play_performance(request, performance_id):
    from .models import StudentPerformance
    from django.contrib import messages
    performance = get_object_or_404(StudentPerformance, id=performance_id)
    
    if performance.student.user != request.user:
        messages.error(request, "Accès refusé.")
        return redirect('home')
        
    return render(request, 'case/play_case.html', {'performance': performance, 'case': performance.case})

@login_required
def performance_detail(request, performance_id):
    from .models import StudentPerformance
    from django.contrib import messages
    performance = get_object_or_404(StudentPerformance, id=performance_id)
    
    if not request.user.is_superuser and performance.student.user != request.user and getattr(request.user, 'role', '') != 'teacher':
        messages.error(request, "Accès refusé.")
        return redirect('home')
        
    return render(request, 'case/performance_detail.html', {'performance': performance})



@login_required
def admin_all_trainings(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    from .models import Training
    from django.http import HttpResponse
    try:
        # Use select_related to avoid N+1 queries which may cause Server crash
        trainings = Training.objects.select_related('case', 'professor__user', 'group').all().order_by('-created_at')
        return render(request, 'administrater/all_trainings.html', {'trainings': trainings})
    except Exception as e:
        import traceback
        error_msg = f"Une erreur s'est produite lors du chargement des entraînements:<br><pre>{traceback.format_exc()}</pre>"
        return HttpResponse(error_msg, status=500)


@login_required
def dynamic_export_csv(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        model_name = request.POST.get('model_name')
        selected_columns = request.POST.getlist('columns')

        if not model_name or not selected_columns:
            messages.error(request, "Veuillez sélectionner au moins une colonne.")
            return redirect('data')

        # Mapping des noms de modèles autorisés
        allowed_models = {
            'Student': 'Student',
            'Professor': 'Professor',
            'StudentPerformance': 'StudentPerformance',
        }

        if model_name not in allowed_models:
            messages.error(request, "Table invalide.")
            return redirect('data')

        try:
            model = apps.get_model('auth_app', allowed_models[model_name])
        except LookupError:
            messages.error(request, "Table invalide.")
            return redirect('data')

        # Labels lisibles pour les colonnes
        field_labels = {
            'user__first_name': 'Prénom',
            'user__last_name': 'Nom',
            'user__email': 'Email',
            'user__username': "Nom d'utilisateur",
            'ine': 'INE',
            'age': 'Âge',
            'gender': 'Genre',
            'degree_level': 'Niveau de diplôme',
            'year_of_study': "Année d'étude",
            'speciality': 'Spécialité',
            'university': 'Université',
            'rgpd_consent': 'Consentement RGPD',
            'scientific_study': 'Consentement étude scientifique',
            'id': 'ID Performance',
            'realization_date': 'Date de réalisation',
            'student__ine': 'INE Étudiant',
            'case__name': 'Cas Clinique',
            'total_score': 'Note totale',
            'clinical_skills_score': 'Notes compétences cliniques',
            'communication_skills_score': 'Notes communication',
            'completion_time': 'Temps de réalisation',
            'is_finished': 'Terminé',
        }

        # Les champs booléens à convertir en Oui/Non
        boolean_fields = {'rgpd_consent', 'scientific_study', 'is_finished'}

        # Prèp ficher csv 
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="export_{model_name.lower()}.csv"'
        response.write('\ufeff')
        writer = csv.writer(response, delimiter=';')

        # En-tête avec les labels lisibles
        header = [field_labels.get(col, col) for col in selected_columns]
        writer.writerow(header)

        # Récupération des données
        if model_name == 'StudentPerformance':
            objects = model.objects.values_list(*selected_columns)
        else:
            objects = model.objects.select_related('user').values_list(*selected_columns)
        for obj in objects:
            row = []
            for i, val in enumerate(obj):
                col_name = selected_columns[i]
                if col_name in boolean_fields:
                    row.append('Oui' if val else 'Non')
                elif val is None:
                    row.append('')
                else:
                    row.append(str(val))
            writer.writerow(row)

        return response

    return redirect('data')

@login_required
def create_case(request):
    if request.method == 'POST':
        from .models import ClinicalCase
        from django.contrib import messages
        
        try:
            professor = request.user.professor_profile
            
            case_obj = ClinicalCase.objects.create(
                creator_professor=professor,
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                reviewer=request.POST.get('reviewer', ''),
                speciality=request.POST.get('speciality', ''),
                study_level=request.POST.get('study_level', ''),
                knowledge_level=request.POST.get('knowledge_level', ''),
                primary_learning_domain=request.POST.get('primary_learning_domain', ''),
                secondary_learning_domain=request.POST.get('secondary_learning_domain', ''),
                objective=request.POST.get('objective', ''),
                briefing_text=request.POST.get('briefing_text', ''),
                instructions_to_do=request.POST.get('instructions_to_do', ''),
                instructions_not_to_do=request.POST.get('instructions_not_to_do', ''),
                has_standardized_patient=request.POST.get('has_standardized_patient') == 'true',
                has_standardized_hcp=request.POST.get('has_standardized_hcp') == 'true',
                has_iconography=request.POST.get('has_iconography') == 'true',
            )
            
            messages.success(request, "Cas créé avec succès.")
            return redirect('case_detail', case_id=case_obj.id)
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du cas: {str(e)}")
            return redirect('create_case')
    
    return render(request, 'teacher/case_creation.html')

@login_required
def teacher_all_trainings(request):
    if request.user.role != 'teacher':
        return redirect('home')

    from .models import StudentPerformance
    from django.db.models import Q
    from django.core.paginator import Paginator

    search_query = request.GET.get('search', '').strip()
    
    performances = StudentPerformance.objects.select_related('student__user', 'case').all().order_by('-realization_date')

    if search_query:
        performances = performances.filter(
            Q(student__user__first_name__icontains=search_query) |
            Q(student__user__last_name__icontains=search_query) |
            Q(case__name__icontains=search_query)
        )

    paginator = Paginator(performances, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'teacher/all_trainings.html', {'performances': page_obj, 'search_query': search_query, 'paginator': paginator})