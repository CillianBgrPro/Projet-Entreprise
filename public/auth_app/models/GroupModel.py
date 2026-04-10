from django.db import models
from auth_app.managers import GroupManager

class Group(models.Model):
    """
    Represents a group of students and professors.
    
    Attributes:
        name (str): The name of the group.
        students (ManyToManyField to Student): A many-to-many relationship with students.
        professors (ManyToManyField to Professor): A many-to-many relationship with professors.
    """

    # Field for storing the name of the group
    name = models.CharField(
        max_length=100, 
        verbose_name="Nom du groupe",
        help_text="The name of the group, should be unique and descriptive."
    )

    # Many-to-many relationship with students
    students = models.ManyToManyField(
        'auth_app.Student', 
        blank=True, 
        related_name='groups', 
        verbose_name="Étudiants"
    )

    # Many-to-many relationship with professors
    professors = models.ManyToManyField(
        'auth_app.Professor', 
        blank=True, 
        related_name='groups', 
        verbose_name="Enseignants"
    )

    # Custom manager for the Group model
    objects = GroupManager()

    def __str__(self):
        return self.name

    class Meta:
        """
        Metadata options for the Group model.
        
        Attributes:
            verbose_name (str): The singular name of the model in the Django admin.
            verbose_name_plural (str): The plural name of the model in the Django admin.
        """
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"