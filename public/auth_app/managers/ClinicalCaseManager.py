from django.db import models

class ClinicalCaseManager(models.Manager):
    """
    Manager for clinical case model, providing methods to filter cases based on various criteria.
    """

    def get_cases_for_study_level(self, level):
        """
        Retrieve all cases that match the given study level.

        Args:
            level (str): The study level to filter by. Case-insensitive.

        Returns:
            QuerySet: A queryset of ClinicalCase objects matching the study level.
        """
        return self.filter(study_level__iexact=level)

    def get_cases_with_standardized_patient(self):
        """
        Retrieve all cases that have a standardized patient.

        Returns:
            QuerySet: A queryset of ClinicalCase objects with a standardized patient.
        """
        return self.filter(has_standardized_patient=True)

    def search(self, name=None, speciality=None, study_level=None, knowledge_level=None, primary_learning_domain=None, date_from=None, date_to=None):
        """
        Search for cases that match the given criteria.

        Args:
            name (str, optional): The name of the case to filter by. Case-insensitive.
            speciality (str, optional): The speciality associated with the case. Case-insensitive.
            study_level (str, optional): The study level to filter by. Case-insensitive.
            knowledge_level (str, optional): The knowledge level to filter by. Case-insensitive.
            primary_learning_domain (str, optional): The primary learning domain of the case. Case-insensitive.
            date_from (date, optional): The start date for filtering cases created on or after this date.
            date_to (date, optional): The end date for filtering cases created on or before this date.

        Returns:
            QuerySet: A queryset of ClinicalCase objects matching the given criteria.
        """
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