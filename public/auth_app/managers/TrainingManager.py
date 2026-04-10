from django.db import models

class TrainingManager(models.Manager):
    """
    This manager provides methods for querying training instances.
    """

    def get_finished_trainings(self):
        """
        Retrieves all trainings that have a status of 'finished' and a non-null finished_at timestamp.

        Returns:
            QuerySet: A queryset containing finished training records.
        """
        return self.filter(status__iexact='finished', finished_at__isnull=False)