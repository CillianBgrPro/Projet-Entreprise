from django.db import models
from auth_app.managers import StudentManager

class Student(models.Model):

    YEAR_CHOICES = [
        ('MM1', 'MM1'),
        ('MM2', 'MM2'),
        ('MM3', 'MM3'),
    ]

    def get_model_universities():
        try:
            import json, os
            from django.conf import settings
            json_path = os.path.join(settings.BASE_DIR, 'universities.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                univs = json.load(f)
            return [(u, u) for u in univs]
        except Exception:
            return [('no univerity found', 'no univerity found')]

    UNIVERSITY_CHOICES = get_model_universities()

    user = models.OneToOneField('auth_app.User', on_delete=models.CASCADE, related_name='student_profile')
    ine = models.IntegerField(verbose_name="INE de l'étudiant")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    degree_level = models.CharField(max_length=20, blank=True, verbose_name="Niveau de diplôme")
    year_of_study = models.CharField(max_length=10, blank=True, null=True, choices=YEAR_CHOICES, verbose_name="Année d'étude")
    speciality = models.CharField(max_length=255, blank=True, verbose_name="Spécialité")
    university = models.CharField(max_length=255, blank=True, choices=UNIVERSITY_CHOICES, verbose_name="Université")
    rgpd_consent = models.BooleanField(default=False, verbose_name="Consentement RGPD")
    scientific_study = models.BooleanField(default=False, verbose_name="Consentement étude scientifique")

    objects = StudentManager()

    def __str__(self):
        return f"Étudiant : {self.user}"

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"