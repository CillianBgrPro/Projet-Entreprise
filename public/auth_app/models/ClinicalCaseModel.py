from django.db import models
from auth_app.managers import ClinicalCaseManager

class ClinicalCase(models.Model):
    """
    Represents a clinical case within the application.
    
    The `ClinicalCase` model holds detailed information about each clinical scenario, including its creator,
    author, reviewer, and various attributes related to the scenario's content, learning objectives, and more.
    """
    
    # ForeignKey to Professor model for the creator of the clinical case
    creator_professor = models.ForeignKey(
        'auth_app.Professor', 
        on_delete=models.CASCADE, 
        related_name='clinical_cases',
        verbose_name="Enseignant créateur"
    )
    
    # String field for the author of the clinical case (optional)
    author = models.CharField(max_length=255, blank=True, verbose_name="Auteur")
    
    # String field for the reviewer of the clinical case (optional)
    reviewer = models.CharField(max_length=255, blank=True, verbose_name="Relecteur")
    
    # String field for the name of the clinical scenario
    name = models.CharField(max_length=255, verbose_name="Titre du scénario")
    
    # String field for the virtual patient ID (optional)
    virtual_patient_id = models.CharField(max_length=255, blank=True, verbose_name="ID patient virtuel")
    
    # String field for the study level (e.g., MM1, MM2, MM3) (optional)
    study_level = models.CharField(
        max_length=255, blank=True,
        verbose_name="Année d'étude",
        help_text="MM1, MM2 ou MM3"
    )
    
    # String field for the knowledge level (e.g., Rang A, Rang B) (optional)
    knowledge_level = models.CharField(
        max_length=255, blank=True,
        verbose_name="Niveau de connaissance",
        help_text="Rang A, Rang B ou Rang A/B"
    )
    
    # String field for the primary learning domain (e.g., Urgence vitale) (optional)
    primary_learning_domain = models.CharField(
        max_length=255, blank=True,
        verbose_name="Domaine d'apprentissage principal",
        help_text="11 domaines possibles (ex: Urgence vitale, Examen clinique)"
    )
    
    # String field for the secondary learning domain (optional)
    secondary_learning_domain = models.CharField(
        max_length=255, blank=True,
        verbose_name="Domaine d'apprentissage secondaire"
    )
    
    # ManyToManyField to StartingSituation model for the starting situations of the clinical case
    starting_situation_id = models.ManyToManyField(
        'auth_app.StartingSituation',
        blank=True,
        verbose_name="Situation de départ",
        help_text="Tableau avec les id des situations de départ"
    )
    
    # String field for the speciality (e.g., Collèges de spécialités) (optional)
    speciality = models.CharField(
        max_length=255, blank=True,
        verbose_name="Spécialité",
        help_text="Collèges de spécialités"
    )
    
    # IntegerField for the item ID in the program (1 to 367) (optional)
    item_id = models.IntegerField(
        blank=True, null=True,
        verbose_name="Item",
        help_text="Chapitre du programme de 1 à 367"
    )
    
    # TextField for the objective of the clinical case
    objective = models.TextField(blank=True, verbose_name="Objectif")
    
    # BooleanField to indicate if there is a standardized patient
    has_standardized_patient = models.BooleanField(default=False, verbose_name="Patient standardisé")
    
    # BooleanField to indicate if there is a standardized HCP (Health Care Provider)
    has_standardized_hcp = models.BooleanField(default=False, verbose_name="Professionnel de santé standardisé")
    
    # BooleanField to indicate if there is iconography associated with the clinical case
    has_iconography = models.BooleanField(default=False, verbose_name="Iconographie")
    
    # String field for the source file path of the ECOS file (optional)
    source_file_path = models.CharField(
        max_length=255, blank=True,
        verbose_name="Fichier source",
        help_text="Fiche d'ECOS source (PDF/Word)"
    )
    
    # TextField for the briefing text
    briefing_text = models.TextField(blank=True, verbose_name="Texte de briefing")
    
    # TextField for instructions to be performed
    instructions_to_do = models.TextField(blank=True, verbose_name="Instructions à réaliser")
    
    # TextField for instructions that should not be followed
    instructions_not_to_do = models.TextField(blank=True, verbose_name="Instructions hors cadre")
    
    # JSONField for the evaluation grid (optional)
    evaluation_grid = models.JSONField(blank=True, null=True, verbose_name="Grille d'évaluation")
    
    # DateTimeField to automatically set the creation date when a record is created
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    # Custom manager for ClinicalCase model
    objects = ClinicalCaseManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cas clinique"
        verbose_name_plural = "Cas cliniques"