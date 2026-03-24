from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        user = authenticate(request, username=u_name, password=p_word)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, 'Identifiants invalides.')
    return render(request, 'connexion.html')

@login_required
def accueil(request):
    return render(request, 'accueil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')