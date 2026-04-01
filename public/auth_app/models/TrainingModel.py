from django.db import models
from auth_app.managers import TrainingManager

class Training(models.Model):
    group = models.ForeignKey('auth_app.Group', on_delete=models.CASCADE, related_name='trainings', verbose_name="Groupe")
    case = models.ForeignKey('auth_app.ClinicalCase', on_delete=models.CASCADE, related_name='trainings', verbose_name="Cas clinique")
    professor = models.ForeignKey('auth_app.Professor', on_delete=models.CASCADE, related_name='trainings', verbose_name="Enseignant")
    status = models.CharField(max_length=20, blank=True, verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de fin")

    objects = TrainingManager()

    def __str__(self):
        return f"Training {self.id} – {self.case.name}"

    class Meta:
        verbose_name = "Entraînement"
        verbose_name_plural = "Entraînements"
