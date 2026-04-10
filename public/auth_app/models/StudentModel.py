from django.db import models
from auth_app.managers import StudentManager

class Student(models.Model):

    YEAR_CHOICES = [
        ('MM1', 'MM1'),
        ('MM2', 'MM2'),
        ('MM3', 'MM3'),
    ]

    # Method to fetch list of universities from a JSON file
    def get_model_universities():
        try:
            import json, os
            from django.conf import settings
            json_path = os.path.join(settings.BASE_DIR, 'universities.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                univs = json.load(f)
            return [(u, u) for u in univs]
        except Exception:
            return [('no university found', 'no university found')]

    # Choices for the university field based on fetched data
    UNIVERSITY_CHOICES = get_model_universities()

    # One-to-one relationship with User model
    user = models.OneToOneField('auth_app.User', on_delete=models.CASCADE, related_name='student_profile')

    # Student identification number
    ine = models.IntegerField(verbose_name="INE de l'étudiant")

    # Age of the student (optional)
    age = models.IntegerField(blank=True, null=True)

    # Gender of the student (optional)
    gender = models.CharField(max_length=10, blank=True)

    # Degree level of the student (optional)
    degree_level = models.CharField(max_length=20, blank=True, verbose_name="Niveau de diplôme")

    # Year of study (optional)
    year_of_study = models.CharField(max_length=10, blank=True, null=True, choices=YEAR_CHOICES, verbose_name="Année d'étude")

    # Speciality of the student (optional)
    speciality = models.CharField(max_length=255, blank=True, verbose_name="Spécialité")

    # University of the student (optional)
    university = models.CharField(max_length=255, blank=True, choices=UNIVERSITY_CHOICES, verbose_name="Université")

    # Boolean field to indicate RGPD consent
    rgpd_consent = models.BooleanField(default=False, verbose_name="Consentement RGPD")

    # Boolean field to indicate scientific study consent
    scientific_study = models.BooleanField(default=False, verbose_name="Consentement étude scientifique")

    # Custom manager for Student model
    objects = StudentManager()

    # String representation of the student object
    def __str__(self):
        return f"Étudiant : {self.user}"

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"