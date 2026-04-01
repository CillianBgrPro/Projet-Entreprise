from django.db import models
from auth_app.managers import ProfessorManager

class Professor(models.Model):
    user = models.OneToOneField('auth_app.User', on_delete=models.CASCADE, related_name='professor_profile')
    speciality = models.CharField(max_length=50, blank=True, verbose_name="Spécialité")
    university = models.CharField(max_length=255, blank=True, verbose_name="Université")
    rgpd_consent = models.BooleanField(default=False, verbose_name="Consentement RGPD")

    objects = ProfessorManager()

    def __str__(self):
        return f"Professeur : {self.user}"

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
