from django.db import models

class StudentPerformanceManager(models.Manager):
    def get_high_scores(self, min_score=15.0):
        """Get performances with a total score greater than or equal to a minimum."""
        return self.filter(total_score__gte=min_score)
