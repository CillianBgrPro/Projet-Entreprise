import random
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db import IntegrityError

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request=request)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                if 'verification_code' in request.session:
                    del request.session['verification_code']
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

@login_required
def accueil(request):
    return render(request, 'accueil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

def envoyer_code_view(request):
    email = request.GET.get('email')
    if email:
        code = str(random.randint(100000, 999999))
        request.session['verification_code'] = code
        request.session['email_a_verifier'] = email
        
        send_mail(
            'Votre code de vérification - DR. VIRTUORL',
            f'Votre code est : {code}',
            'noreply@virtuorl.fr',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'Email manquant'})