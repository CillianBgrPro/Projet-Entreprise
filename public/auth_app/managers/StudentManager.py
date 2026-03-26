from django.db import models

class StudentManager(models.Manager):
    def get_consented_students(self):
        """Get students who have accepted the RGPD."""
        return self.filter(rgpd_consent=True)
        
    def get_by_university(self, university_name):
        """Get students from a specific university."""
        return self.filter(university__icontains=university_name)
