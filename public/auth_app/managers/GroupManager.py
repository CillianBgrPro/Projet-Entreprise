from django.db import models

class GroupManager(models.Manager):
    """
    Custom manager for the Group model.
    
    This manager includes a method to retrieve groups that have at least one student assigned to them.
    """

    def get_groups_with_students(self):
        """
        Returns a queryset of groups that have at least one student associated with them.

        :return: Queryset of groups with students
        :rtype: django.db.models.query.QuerySet
        """
        return self.filter(students__isnull=False).distinct()