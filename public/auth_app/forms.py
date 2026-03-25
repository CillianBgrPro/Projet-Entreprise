from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    verification_code = forms.CharField(label="Code de vérification", max_length=6)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "last_name", "first_name", "email", "university", "study_year")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].required = False

    def clean_verification_code(self):
        code_saisi = self.cleaned_data.get('verification_code')
        code_attendu = self.request.session.get('verification_code')
        
        if not code_attendu or code_saisi != code_attendu:
            raise forms.ValidationError("Le code de vérification est incorrect ou a expiré.")
        return code_saisi
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Un compte avec cette adresse email existe déjà.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user