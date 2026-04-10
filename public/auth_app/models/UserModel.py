from django.contrib.auth.models import AbstractUser
from django.db import models
from auth_app.managers import UserManager

# Custom User model extending Django's built-in AbstractUser model
class User(AbstractUser):
    """
    Represents a user in the system with additional fields for role, email verification,
    two-factor authentication, and avatar.
    
    Fields:
        - role (CharField): A string representing the user's role in the system.
        - email_verify (BooleanField): A boolean indicating whether the user has verified their email address.
        - a2f (BooleanField): A boolean indicating whether the user has enabled two-factor authentication.
        - avatar (CharField): A string representing the user's avatar image path.
    
    Methods:
        __str__ (method): Returns a string representation of the user, which includes the user's first and last name.
    """
    
    role = models.CharField(max_length=20, blank=True, verbose_name="Rôle")
    email_verify = models.BooleanField(default=False, verbose_name="Email vérifié")
    a2f = models.BooleanField(default=False, verbose_name="Authentification à deux facteurs")
    avatar = models.CharField(max_length=50, default='person', verbose_name="Avatar")

    # Custom manager for User model
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of the user.
        
        Returns:
            str: A string in the format 'First Name Last Name'
        """
        return f"{self.first_name} {self.last_name}"