from django.db import models

class ProfessorManager(models.Manager):
    def get_by_speciality(self, speciality_name):
        """Get professors by speciality."""
        return self.filter(speciality__icontains=speciality_name)

    