from django.db import models

class StudentManager(models.Manager):
    def get_consented_students(self):
        """Get students who have accepted the RGPD."""
        return self.filter(rgpd_consent=True)
        
    def get_by_university(self, university_name):
        """Get students from a specific university."""
        return self.filter(university__icontains=university_name)


class ClinicalCaseManager(models.Manager):
    def get_cases_for_study_level(self, level):
        """Get cases for a specific study level"""
        return self.filter(study_level__iexact=level)
        
    def get_cases_with_standardized_patient(self):
        """Get patient were patient with interaction"""
        return self.filter(has_standardized_patient=True)
