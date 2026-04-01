from django.db import models
from auth_app.managers import ClinicalCaseManager

class ClinicalCase(models.Model):
    creator_professor = models.ForeignKey(
        'auth_app.Professor', on_delete=models.CASCADE, related_name='clinical_cases',
        verbose_name="Enseignant créateur"
    )
    author = models.CharField(max_length=255, blank=True, verbose_name="Auteur")
    reviewer = models.CharField(max_length=255, blank=True, verbose_name="Relecteur")
    name = models.CharField(max_length=255, verbose_name="Titre du scénario")
    virtual_patient_id = models.CharField(max_length=255, blank=True, verbose_name="ID patient virtuel")
    study_level = models.CharField(
        max_length=255, blank=True,
        verbose_name="Année d'étude",
        help_text="MM1, MM2 ou MM3"
    )
    knowledge_level = models.CharField(
        max_length=255, blank=True,
        verbose_name="Niveau de connaissance",
        help_text="Rang A, Rang B ou Rang A/B"
    )
    primary_learning_domain = models.CharField(
        max_length=255, blank=True,
        verbose_name="Domaine d'apprentissage principal",
        help_text="11 domaines possibles (ex: Urgence vitale, Examen clinique)"
    )
    secondary_learning_domain = models.CharField(
        max_length=255, blank=True,
        verbose_name="Domaine d'apprentissage secondaire"
    )
    starting_situation_id = models.CharField(
        max_length=255, blank=True,
        verbose_name="Situation de départ",
        help_text="Classement de 1 à 356"
    )
    speciality = models.CharField(
        max_length=255, blank=True,
        verbose_name="Spécialité",
        help_text="Collèges de spécialités"
    )
    item_id = models.IntegerField(
        blank=True, null=True,
        verbose_name="Item",
        help_text="Chapitre du programme de 1 à 367"
    )
    objective = models.TextField(blank=True, verbose_name="Objectif")
    has_standardized_patient = models.BooleanField(default=False, verbose_name="Patient standardisé")
    has_standardized_hcp = models.BooleanField(default=False, verbose_name="Professionnel de santé standardisé")
    has_iconography = models.BooleanField(default=False, verbose_name="Iconographie")
    source_file_path = models.CharField(
        max_length=255, blank=True,
        verbose_name="Fichier source",
        help_text="Fiche d'ECOS source (PDF/Word)"
    )
    briefing_text = models.TextField(blank=True, verbose_name="Texte de briefing")
    instructions_to_do = models.TextField(blank=True, verbose_name="Instructions à réaliser")
    instructions_not_to_do = models.TextField(blank=True, verbose_name="Instructions hors cadre")
    evaluation_grid = models.JSONField(blank=True, null=True, verbose_name="Grille d'évaluation")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    objects = ClinicalCaseManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cas clinique"
        verbose_name_plural = "Cas cliniques"
