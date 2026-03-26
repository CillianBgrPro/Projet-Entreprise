from django.db import models
from auth_app.managers import StudentManager

class Student(models.Model):
    """Étudiant."""
    user = models.OneToOneField('auth_app.User', on_delete=models.CASCADE, related_name='student_profile')
    ine = models.IntegerField(verbose_name="INE de l'étudiant")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    degree_level = models.CharField(max_length=20, blank=True, verbose_name="Niveau de diplôme")
    year_of_study = models.IntegerField(blank=True, null=True, verbose_name="Année d'étude")
    speciality = models.CharField(max_length=255, blank=True, verbose_name="Spécialité")
    university = models.CharField(max_length=255, blank=True, verbose_name="Université")
    rgpd_consent = models.BooleanField(default=False, verbose_name="Consentement RGPD")

    objects = StudentManager()

    def __str__(self):
        return f"Étudiant : {self.user}"

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
