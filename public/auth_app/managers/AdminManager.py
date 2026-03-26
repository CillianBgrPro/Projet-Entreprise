from django.db import models

class AdminManager(models.Manager):
    def get_all_admins(self):
        """Get all admins."""
        return self.all()
