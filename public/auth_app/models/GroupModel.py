from django.db import models
from auth_app.managers import GroupManager

class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du groupe")
    students = models.ManyToManyField('auth_app.Student', blank=True, related_name='groups', verbose_name="Étudiants")
    professors = models.ManyToManyField('auth_app.Professor', blank=True, related_name='groups', verbose_name="Enseignants")

    objects = GroupManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"
