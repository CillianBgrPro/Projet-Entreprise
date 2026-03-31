import time
import random
import django
import resend
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.contrib.auth import logout
import csv

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request=request)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                request.session.pop('verification_code', None)
                request.session.pop('verification_code_time', None)
                return redirect('accueil')
            except IntegrityError:
                form.add_error(None, "Une erreur est survenue : cet utilisateur existe probablement déjà.")
    else:
        form = CustomUserCreationForm(request=request)
    
    return render(request, 'connexion/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        if u_name:
            u_name = u_name.strip().lower() 

        user = authenticate(request, username=u_name, password=p_word)

        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            from .models import User
            user_exists = User.objects.filter(username=u_name).exists()
            if not user_exists:
                messages.error(request, "Ce compte n'existe pas.")
            else:
                messages.error(request, "Mot de passe incorrect.")
    
    return render(request, 'connexion/connexion.html')

def accueil(request):
    # logout(request)
    return render(request, 'accueil.html')

@login_required
def compte(request):
    """Redirige vers le bon dashboard selon le rôle de l'utilisateur."""
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('accueil')
    return render(request, 'dashboard.html')

def deconnexion(request):
    logout(request)
    return redirect('accueil')

def users(request):
    if not request.user.is_superuser:
        return redirect('accueil')
    
    from .models import User
    users = User.objects.all()
    return render(request, 'administrater/users.html', {'users': users})

def logs(request):
    if not request.user.is_superuser:
        return redirect('accueil')
    
    return render(request, 'administrater/logs.html')

def data(request):
    if not request.user.is_superuser:
        return redirect('accueil')
    
    return render(request, 'administrater/data.html')

def envoyer_code_view(request):
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

def verifier_code(request):
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
        return redirect('accueil')
        
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