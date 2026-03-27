from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    verification_code = forms.CharField(label="Code de vérification", max_length=6, required=True)
    university = forms.CharField(label="Université", required=False)
    study_year = forms.IntegerField(label="Année d'étude", required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "last_name", "first_name", "email")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].required = False


    # def clean_verification_code(self):
    #     code_saisi = self.cleaned_data.get('verification_code')
    #     code_attendu = self.request.session.get('verification_code')
        
    #     if not code_attendu or code_saisi != code_attendu:
    #         raise forms.ValidationError("Le code de vérification est incorrect ou a expiré.")
    #     return code_saisi

    def clean_verification_code(self):
        import time
        code_saisi = self.cleaned_data.get('verification_code', '').strip()
        code_attendu = self.request.session.get('verification_code') if self.request else None
        code_timestamp = self.request.session.get('verification_code_time', 0) if self.request else 0

        if not code_attendu:
            raise forms.ValidationError("Aucun code envoyé. Veuillez cliquer sur \"Envoyer le code\" d'abord.")

        # Expiration après 10 minutes
        if time.time() - code_timestamp > 600:
            raise forms.ValidationError("Le code a expiré. Veuillez en demander un nouveau.")

        if code_saisi != code_attendu:
            raise forms.ValidationError("Code de vérification incorrect.")

        return code_saisi
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Un compte avec cette adresse email existe déjà.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email').lower()
        user.username = email
        user.email = email
        user.role = 'student'
        if commit:
            user.save()
            from .models import Student
            university = self.cleaned_data.get('university')
            study_year = self.cleaned_data.get('study_year')
            Student.objects.create(
                user=user,
                ine=0,  # par defaut
                university=university if university else "",
                year_of_study=study_year if study_year else None
            )
        return user