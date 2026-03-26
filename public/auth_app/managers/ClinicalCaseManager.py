from django.db import models

class ClinicalCaseManager(models.Manager):
    def get_cases_for_study_level(self, level):
        """Get cases for a specific study level"""
        return self.filter(study_level__iexact=level)
        
    def get_cases_with_standardized_patient(self):
        """Get patient were patient with interaction"""
        return self.filter(has_standardized_patient=True)
