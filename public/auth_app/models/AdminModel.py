from django.db import models
from auth_app.managers import AdminManager

class Admin(models.Model):
    user = models.OneToOneField('auth_app.User', on_delete=models.CASCADE, related_name='admin_profile')

    objects = AdminManager()

    def __str__(self):
        return f"Admin : {self.user}"

    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"
