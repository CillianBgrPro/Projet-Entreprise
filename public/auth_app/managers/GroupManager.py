from django.db import models

class GroupManager(models.Manager):
    def get_groups_with_students(self):
        """Get groups with at least one student."""
        return self.filter(students__isnull=False).distinct()
