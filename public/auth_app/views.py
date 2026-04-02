import time
import random
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
import csv

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
    return render(request, 'dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def users(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    from .models import User
    users = User.objects.all()
    return render(request, 'administrater/users.html', {'users': users})

def logs(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    return render(request, 'administrater/logs.html')

def data(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    return render(request, 'administrater/data.html')

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
    tickets = Ticket.objects.all().order_by('-created_at')
    return render(request, 'administrater/ticket_admin.html', {'tickets': tickets})

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
    cases = ClinicalCase.objects.all()
    return render(request, 'case/all_case.html', {'cases': cases})

@login_required
def case_detail(request, case_id):
    from .models import ClinicalCase
    case_obj = get_object_or_404(ClinicalCase, id=case_id)
    return render(request, 'case/case_detail.html', {'case': case_obj})