from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import StudentManager, ClinicalCaseManager


class User(AbstractUser):
    """Utilisateur de la plateforme."""
    role = models.CharField(max_length=20, blank=True, verbose_name="Rôle")
    email_verify = models.BooleanField(default=False, verbose_name="Email vérifié")
    a2f = models.BooleanField(default=False, verbose_name="Authentification à deux facteurs")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    """Étudiant."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
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


class Professor(models.Model):
    """Enseignant."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    speciality = models.CharField(max_length=50, blank=True, verbose_name="Spécialité")
    university = models.CharField(max_length=255, blank=True, verbose_name="Université")
    rgpd_consent = models.BooleanField(default=False, verbose_name="Consentement RGPD")

    def __str__(self):
        return f"Professeur : {self.user}"

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"


class Admin(models.Model):
    """Administrateur."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return f"Admin : {self.user}"

    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"


class Group(models.Model):
    """Groupe d'utilisateurs."""
    name = models.CharField(max_length=100, verbose_name="Nom du groupe")
    students = models.ManyToManyField(Student, blank=True, related_name='groups', verbose_name="Étudiants")
    professors = models.ManyToManyField(Professor, blank=True, related_name='groups', verbose_name="Enseignants")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"


class ClinicalCase(models.Model):
    """Cas clinique ECOS."""
    creator_professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name='clinical_cases',
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


class Training(models.Model):
    """Entraînement (session de cas clinique pour un groupe)."""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='trainings', verbose_name="Groupe")
    case = models.ForeignKey(ClinicalCase, on_delete=models.CASCADE, related_name='trainings', verbose_name="Cas clinique")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='trainings', verbose_name="Enseignant")
    status = models.CharField(max_length=20, blank=True, verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de fin")

    def __str__(self):
        return f"Training {self.id} – {self.case.name}"

    class Meta:
        verbose_name = "Entraînement"
        verbose_name_plural = "Entraînements"


class StudentPerformance(models.Model):
    """Performance d'un étudiant sur un cas clinique."""
    realization_date = models.DateTimeField(verbose_name="Date de réalisation")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performances', verbose_name="Étudiant")
    case = models.ForeignKey(ClinicalCase, on_delete=models.CASCADE, related_name='performances', verbose_name="Cas clinique")
    total_score = models.FloatField(blank=True, null=True, verbose_name="Score total")
    clinical_skills_score = models.FloatField(blank=True, null=True, verbose_name="Score compétences cliniques")
    communication_skills_score = models.FloatField(blank=True, null=True, verbose_name="Score communication")
    completion_time = models.DurationField(blank=True, null=True, verbose_name="Temps de complétion")
    conversation_log = models.JSONField(
        blank=True, null=True,
        verbose_name="Log de conversation",
        help_text="Log du dialogue avec l'agent (JSON)"
    )
    evaluation_log = models.JSONField(
        blank=True, null=True,
        verbose_name="Log d'évaluation",
        help_text="Log du débriefing avec l'agent évaluateur (JSON)"
    )

    def __str__(self):
        return f"Performance {self.student} – {self.case.name}"

    class Meta:
        verbose_name = "Performance étudiant"
        verbose_name_plural = "Performances étudiants"


class Ticket(models.Model):
    """Ticket de support."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', verbose_name="Utilisateur")
    subject = models.CharField(max_length=150, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    status = models.CharField(max_length=20, blank=True, verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f"[{self.status}] {self.subject}"

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"