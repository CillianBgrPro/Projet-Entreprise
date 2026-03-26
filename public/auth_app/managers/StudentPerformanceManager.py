from django.db import models
from django.db.models import Avg, Max, Count

class StudentPerformanceManager(models.Manager):

    def get_high_scores(self, min_score=15.0):
        return self.filter(total_score__gte=min_score)

    def get_student_history(self, student):
        return self.filter(student=student).order_by('-realization_date')

    def get_best_performance(self, student, case):

        return self.filter(student=student, case=case).order_by('-total_score').first()

    def get_student_stats(self, student):
        return self.filter(student=student).aggregate(
            moyenne_totale=Avg('total_score'),
            moyenne_clinique=Avg('clinical_skills_score'),
            moyenne_comm=Avg('communication_skills_score'),
            nombre_tentatives=Count('id')
        )


    def get_weak_communication_scores(self, threshold=10.0):
        return self.filter(communication_skills_score__lt=threshold)

    def get_case_average(self, case):
        return self.filter(case=case).aggregate(Avg('total_score'))['total_score__avg']

    def get_fastest_completions(self, case, limit=5):
        return self.filter(case=case).order_by('completion_time')[:limit]