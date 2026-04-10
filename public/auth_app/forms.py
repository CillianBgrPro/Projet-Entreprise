from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form that extends Django's built-in `UserCreationForm`.
    
    This form includes additional fields such as a verification code, university selection,
    study year, INE (French National Identification Number), consent checkbox, and a field
    for scientific studies.
    """

    # Verification code field
    verification_code = forms.CharField(label="Code de vérification", max_length=6, required=True)

    @staticmethod
    def get_universities():
        """
        Retrieves universities from a JSON file located in the Django project's settings directory.

        Returns:
            list: A list of university choices formatted as tuples for use in form fields.
        """
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

    # University choices
    UNIVERSITY_CHOICES = get_universities()

    # Year choices
    YEAR_CHOICES = [
        ('', '— Sélectionnez votre année —'),
        ('DFASM1', 'DFASM1'),
        ('DFASM2', 'DFASM2'),
        ('DFASM3', 'DFASM3'),
    ]

    # University field
    university = forms.ChoiceField(label="Université", choices=UNIVERSITY_CHOICES, required=False, widget= forms.Select(attrs={'tabindex': '3'}))
    
    # Study year field
    study_year = forms.ChoiceField(label="Année d'étude", choices=YEAR_CHOICES, required=False, widget= forms.Select(attrs={'tabindex': '4'}))

    # INE (French National Identification Number) field
    ine = forms.CharField(
        label="INE",
        required=True,
        strip=True,
        widget=forms.TextInput(attrs={"inputmode": "numeric", "pattern": "[0-9]{10}"}),
    )

    # Consent checkbox field
    consent = forms.BooleanField(required=True)
    
    # Scientific studies checkbox field
    scientific_study = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        """
        Meta class that specifies the model and fields to be used by this form.
        
        Args:
            model (User): The Django user model.
            fields (tuple): A tuple containing the fields to be included in the form.
                These fields are username, last_name, first_name, and email.
        """
        model = User
        fields = ("username", "last_name", "first_name", "email")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Make username field optional if it exists
        if 'username' in self.fields:
            self.fields['username'].required = False
        
        # Update university choices dynamically
        self.fields['university'].choices = self.get_universities()

    def clean_verification_code(self):
        """
        Validates the verification code entered by the user.
        
        Returns:
            str: The cleaned verification code.

        Raises:
            forms.ValidationError: If the verification code is missing, expired, or incorrect.
        """
        import time
        code_saisi = self.cleaned_data.get('verification_code', '').strip()
        code_attendu = self.request.session.get('verification_code') if self.request else None
        code_timestamp = self.request.session.get('verification_code_time', 0) if self.request else 0

        if not code_attendu:
            raise forms.ValidationError("Aucun code envoyé. Veuillez cliquer sur \"Envoyer le code\" d'abord.")

        # Expiration after 10 minutes
        if time.time() - code_timestamp > 600:
            raise forms.ValidationError("Le code a expiré. Veuillez en demander un nouveau.")

        if code_saisi != code_attendu:
            raise forms.ValidationError("Code de vérification incorrect.")

        return code_saisi
    
    def clean_email(self):
        """
        Validates the email entered by the user.
        
        Returns:
            str: The cleaned and lowercased email.

        Raises:
            forms.ValidationError: If an account with this email already exists.
        """
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Un compte avec cette adresse email existe déjà.")
        return email

    def clean_ine(self):
        """
        Validates the INE (French National Identification Number) entered by the user.
        
        Returns:
            int: The cleaned and validated INE number.

        Raises:
            forms.ValidationError: If the INE is not numeric or does not contain exactly 10 digits.
        """
        ine_raw = (self.cleaned_data.get("ine") or "").strip()
        if not ine_raw.isdigit():
            raise forms.ValidationError("Veuillez saisir un INE valide.")
        # INE (Identifiant National Étudiant) : 10 chiffres.
        if len(ine_raw) != 10:
            raise forms.ValidationError("L'INE doit contenir 10 chiffres.")
        return int(ine_raw)
    
    def save(self, commit=True):
        """
        Saves the user and associated student data to the database.

        Args:
            commit (bool): Whether to commit the changes to the database. Defaults to True.

        Returns:
            User: The saved user instance.
        """
        user = super().save(commit=False)
        email = self.cleaned_data.get('email').lower()
        user.username = email
        user.email = email
        user.role = 'student'
        
        if commit:
            user.save()
            from .models import Student
            
            # Create associated student record
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


class ChangePasswordForm(forms.Form):
    """
    A form for changing a user's password.
    
    This form includes fields for the old password, new password, and confirmation of the new password.
    It also performs validation to ensure that the new passwords match and that the old password is correct.
    """

    # Old password field
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        label="ancien mot de pase"
    )

    # New password field
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        label="new mot de passe"
    )

    # Confirm password field
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        label="confirmé le mot de passe"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validates the old password entered by the user.
        
        Returns:
            str: The cleaned old password.

        Raises:
            forms.ValidationError: If the old password is incorrect.
        """
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("L'ancien mot de passe est incorrect.")
        return old_password

    def clean(self):
        """
        Cleans and validates form data, ensuring that the new passwords match.
        
        Returns:
            dict: The cleaned data.

        Raises:
            forms.ValidationError: If the new passwords do not match.
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "Les deux mots de passe ne correspondent pas.")
        return cleaned_data