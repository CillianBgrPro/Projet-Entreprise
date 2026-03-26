from django.contrib.auth.models import UserManager as DefaultUserManager

class UserManager(DefaultUserManager):
    def get_verified_users(self):
        """Get users who have verified their email."""
        return self.filter(email_verify=True)
