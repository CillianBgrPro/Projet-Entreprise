from django.db import models

class ProfessorManager(models.Manager):
    """
    Custom manager for the Professor model.
    
    Provides a method to retrieve professors by their speciality.
    """

    def get_by_speciality(self, speciality_name):
        """
        Get professors whose speciality contains the specified name.

        :param speciality_name: The partial or full name of the speciality.
        :type speciality_name: str
        :return: A queryset containing professors matching the speciality criteria.
        :rtype: QuerySet[Professor]
        """
        return self.filter(speciality__icontains=speciality_name)