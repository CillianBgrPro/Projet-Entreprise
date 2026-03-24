from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    university = models.CharField(max_length=100, blank=True, verbose_name="Université")
    study_year = models.CharField(max_length=50, blank=True, verbose_name="Année d'étude")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"