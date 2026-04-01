from django.contrib.auth.models import AbstractUser
from django.db import models
from auth_app.managers import UserManager

class User(AbstractUser):
    role = models.CharField(max_length=20, blank=True, verbose_name="Rôle")
    email_verify = models.BooleanField(default=False, verbose_name="Email vérifié")
    a2f = models.BooleanField(default=False, verbose_name="Authentification à deux facteurs")

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
