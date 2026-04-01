from django.db import models

class TrainingManager(models.Manager):
    def get_finished_trainings(self):
        #Get finished trainings.
        return self.filter(status__iexact='finished', finished_at__isnull=False)
