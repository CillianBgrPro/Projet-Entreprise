from django.db import models
from auth_app.managers import StudentPerformanceManager

class StudentPerformance(models.Model):
    realization_date = models.DateTimeField(verbose_name="Date de réalisation")
    student = models.ForeignKey('auth_app.Student', on_delete=models.CASCADE, related_name='performances', verbose_name="Étudiant")
    case = models.ForeignKey('auth_app.ClinicalCase', on_delete=models.CASCADE, related_name='performances', verbose_name="Cas clinique")
    total_score = models.FloatField(blank=True, null=True, verbose_name="Note totale")
    clinical_skills_score = models.FloatField(blank=True, null=True, verbose_name="Notes compétences cliniques")
    communication_skills_score = models.FloatField(blank=True, null=True, verbose_name="Notes communication")
    completion_time = models.DurationField(blank=True, null=True, verbose_name="Temps de réalisation")
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

    objects = StudentPerformanceManager()

    def __str__(self):
        return f"Performance {self.student} – {self.case.name}"

    class Meta:
        verbose_name = "Performance étudiant"
        verbose_name_plural = "Performances étudiants"
