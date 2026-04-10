from django.db import models
from auth_app.managers import StudentPerformanceManager

class StudentPerformance(models.Model):
    """
    Model representing the performance of a student in a clinical case.
    """

    # Date and time when the performance was realized
    realization_date = models.DateTimeField(verbose_name="Date de réalisation")

    # Foreign key to the Student model, related name 'performances'
    student = models.ForeignKey('auth_app.Student', on_delete=models.CASCADE, related_name='performances', verbose_name="Étudiant")

    # Foreign key to the ClinicalCase model, related name 'performances'
    case = models.ForeignKey('auth_app.ClinicalCase', on_delete=models.CASCADE, related_name='performances', verbose_name="Cas clinique")

    # Total score obtained by the student
    total_score = models.FloatField(blank=True, null=True, verbose_name="Note totale")

    # Score for clinical skills
    clinical_skills_score = models.FloatField(blank=True, null=True, verbose_name="Notes compétences cliniques")

    # Score for communication skills
    communication_skills_score = models.FloatField(blank=True, null=True, verbose_name="Notes communication")

    # Duration of the performance
    completion_time = models.DurationField(blank=True, null=True, verbose_name="Temps de réalisation")

    # Log of conversation with the agent (JSON format)
    conversation_log = models.JSONField(
        blank=True, null=True,
        verbose_name="Log de conversation",
        help_text="Log du dialogue avec l'agent (JSON)"
    )

    # Log of evaluation by the evaluator (JSON format)
    evaluation_log = models.JSONField(
        blank=True, null=True,
        verbose_name="Log d'évaluation",
        help_text="Log du débriefing avec l'agent évaluateur (JSON)"
    )

    # Boolean field indicating if the performance is finished
    is_finished = models.BooleanField(default=False, verbose_name="Finished")

    # Custom manager for the model
    objects = StudentPerformanceManager()

    def __str__(self):
        """
        String representation of the model.
        
        Returns:
            str: A string in the format "Performance {student} – {case.name}"
        """
        return f"Performance {self.student} – {self.case.name}"

    class Meta:
        verbose_name = "Performance étudiant"
        verbose_name_plural = "Performances étudiants"