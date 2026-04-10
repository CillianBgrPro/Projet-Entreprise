from django.db import models
from auth_app.managers import ProfessorManager

class Professor(models.Model):
    """
    Represents a professor in the system.
    """

    # One-to-one relationship with the User model
    user = models.OneToOneField(
        'auth_app.User', 
        on_delete=models.CASCADE, 
        related_name='professor_profile',
        verbose_name="Utilisateur associé"
    )

    # Speciality of the professor
    speciality = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Spécialité"
    )

    # University where the professor is affiliated
    university = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name="Université"
    )

    # Consent for RGPD (General Data Protection Regulation)
    rgpd_consent = models.BooleanField(
        default=False, 
        verbose_name="Consentement RGPD"
    )

    # Custom manager for the Professor model
    objects = ProfessorManager()

    def __str__(self):
        return f"Professeur : {self.user}"

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"