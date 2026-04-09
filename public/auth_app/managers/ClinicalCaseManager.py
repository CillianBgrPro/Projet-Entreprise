from django.db import models

class ClinicalCaseManager(models.Manager):
    def get_cases_for_study_level(self, level):
        return self.filter(study_level__iexact=level)
        
    def get_cases_with_standardized_patient(self):
        return self.filter(has_standardized_patient=True)

    def search(self, name=None, speciality=None, study_level=None, knowledge_level=None, primary_learning_domain=None, date_from=None, date_to=None):
        qs = self.all()
        if name:
            qs = qs.filter(name__icontains=name)
        if speciality:
            qs = qs.filter(speciality__icontains=speciality)
        if study_level:
            qs = qs.filter(study_level__iexact=study_level)
        if knowledge_level:
            qs = qs.filter(knowledge_level__iexact=knowledge_level)
        if primary_learning_domain:
            qs = qs.filter(primary_learning_domain__icontains=primary_learning_domain)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        return qs
