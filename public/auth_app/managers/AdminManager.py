from django.db import models
from django.db.models import Q

class AdminManager(models.Manager):
    
    def get_cases_for_study_level(self, level):
        return self.filter(study_level__iexact=level)
        
    def get_cases_with_standardized_patient(self):
        return self.filter(has_standardized_patient=True)

    def get_recent_cases(self, limit=10):
        return self.all().order_by('-created_at')[:limit]

    def search_cases(self, query):
        return self.filter(
            Q(name__icontains=query) | 
            Q(author__icontains=query) | 
            Q(speciality__icontains=query)
        ).distinct()

    def get_by_knowledge_rank(self, rank):
        return self.filter(knowledge_level__icontains=rank)

    def get_cases_by_speciality(self, spec):
        return self.filter(speciality__icontains=spec)

    def get_pending_review(self):
        return self.filter(reviewer__isnull=True) | self.filter(reviewer='')

    def get_full_multimedia_cases(self):
        return self.filter(has_iconography=True).exclude(virtual_patient_id='')

    def get_by_professor(self, professor_id):
        return self.filter(creator_professor_id=professor_id)