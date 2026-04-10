from django.db import models
from django.db.models import Avg, Max, Count

class StudentPerformanceManager(models.Manager):

    def get_high_scores(self, min_score=15.0):
        """Returns students with a total score greater than or equal to the specified minimum score."""
        return self.filter(total_score__gte=min_score)

    def get_student_history(self, student):
        """Retrieves performance history for a specific student, sorted by realization date in descending order."""
        return self.filter(student=student).order_by('-realization_date')

    def get_best_performance(self, student, case):
        """Finds the best performance record for a specific student and case, ordered by total score in descending order."""
        return self.filter(student=student, case=case).order_by('-total_score').first()

    def get_student_stats(self, student):
        """Aggregates statistics for a specific student's performances."""
        return self.filter(student=student).aggregate(
            moyenne_totale=Avg('total_score'),
            moyenne_clinique=Avg('clinical_skills_score'),
            moyenne_comm=Avg('communication_skills_score'),
            nombre_tentatives=Count('id')
        )

    def get_weak_communication_scores(self, threshold=10.0):
        """Retrieves students with communication skills scores below a specified threshold."""
        return self.filter(communication_skills_score__lt=threshold)

    def get_case_average(self, case):
        """Calculates the average total score for all performances in a specific case."""
        return self.filter(case=case).aggregate(Avg('total_score'))['total_score__avg']

    def get_fastest_completions(self, case, limit=5):
        """Retrieves the fastest completions of a specific case, up to a specified limit, ordered by completion time."""
        return self.filter(case=case).order_by('completion_time')[:limit]