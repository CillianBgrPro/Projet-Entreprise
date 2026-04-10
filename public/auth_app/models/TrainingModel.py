from django.db import models
from auth_app.managers import TrainingManager

class Training(models.Model):
    """
    Represents a training session in the system.
    
    This model is used to store information about each training event, including 
    the associated group, clinical case, professor, status, and timestamps for creation 
    and completion.
    """

    # ForeignKey relationships
    group = models.ForeignKey(
        'auth_app.Group',  # The related model
        on_delete=models.CASCADE,  # What to do when the related object is deleted
        related_name='trainings',  # Name for the reverse relation from Group
        verbose_name="Groupe"  # Human-readable name for admin interface and form fields
    )

    case = models.ForeignKey(
        'auth_app.ClinicalCase',
        on_delete=models.CASCADE,
        related_name='trainings',
        verbose_name="Cas clinique"
    )

    professor = models.ForeignKey(
        'auth_app.Professor',
        on_delete=models.CASCADE,
        related_name='trainings',
        verbose_name="Enseignant"
    )

    # CharField for status
    status = models.CharField(
        max_length=20,  # Maximum length of the string
        blank=True,  # Allow this field to be empty
        verbose_name="Statut"  # Human-readable name for admin interface and form fields
    )

    # DateTimeField for creation timestamp
    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically set on object creation
        verbose_name="Date de création"
    )

    # DateTimeField for completion timestamp
    finished_at = models.DateTimeField(
        blank=True,  # Allow this field to be empty
        null=True,  # Allow this field to have a NULL value
        verbose_name="Date de fin"
    )

    # Custom manager for the model
    objects = TrainingManager()

    # String representation of the object
    def __str__(self):
        return f"Training {self.id} – {self.case.name}"

    class Meta:
        """
        Metadata options for the model.
        
        This inner class is used to provide additional metadata for the model, such as 
        verbose names and plural forms.
        """
        verbose_name = "Entraînement"
        verbose_name_plural = "Entraînements"