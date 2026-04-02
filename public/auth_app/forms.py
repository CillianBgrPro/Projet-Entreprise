from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    verification_code = forms.CharField(label="Code de vérification", max_length=6, required=True)

    @staticmethod
    def get_universities():
        try:
            import json, os
            from django.conf import settings
            json_path = os.path.join(settings.BASE_DIR, 'universities.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                univs = json.load(f)
                liste_univeristy = univs.get('medical_university_france', [])
            return [('', '— Sélectionnez votre université —')] + [(u['university_name'], u['university_name']) for u in liste_univeristy]
        except Exception:
            return [
                ('Aucune université trouvée', 'Aucune université trouvée')
            ]

    UNIVERSITY_CHOICES = get_universities()

    YEAR_CHOICES = [
        ('', '— Sélectionnez votre année —'),
        ('DFASM1', 'DFASM1'),
        ('DFASM2', 'DFASM2'),
        ('DFASM3', 'DFASM3'),
    ]

    university = forms.ChoiceField(label="Université", choices=UNIVERSITY_CHOICES, required=False, widget= forms.Select(attrs={'tabindex': '3'}))
    study_year = forms.ChoiceField(label="Année d'étude", choices=YEAR_CHOICES, required=False, widget= forms.Select(attrs={'tabindex': '4'}))
    ine = forms.CharField(
        label="INE",
        required=True,
        strip=True,
        widget=forms.TextInput(attrs={"inputmode": "numeric", "pattern": "[0-9]{10}"}),
    )
    consent = forms.BooleanField(required=True)
    scientific_study = forms.BooleanField(required=False)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "last_name", "first_name", "email")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].required = False
        self.fields['university'].choices = self.get_universities()

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

    def clean_ine(self):
        ine_raw = (self.cleaned_data.get("ine") or "").strip()
        if not ine_raw.isdigit():
            raise forms.ValidationError("Veuillez saisir un INE valide.")
        # INE (Identifiant National Étudiant) : 10 chiffres.
        if len(ine_raw) != 10:
            raise forms.ValidationError("L'INE doit contenir 10 chiffres.")
        return int(ine_raw)
    
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
            ine = self.cleaned_data.get("ine")
            consent = self.cleaned_data.get('consent', False)
            scientific_study = self.cleaned_data.get('scientific_study', False)
            Student.objects.create(
                user=user,
                ine=ine,
                university=university if university else "",
                year_of_study=study_year if study_year else None,
                rgpd_consent=consent,
                scientific_study=scientific_study
            )
        return user