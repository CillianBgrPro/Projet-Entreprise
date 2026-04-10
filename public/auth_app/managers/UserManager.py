from django.contrib.auth.models import UserManager as DefaultUserManager

class UserManager(DefaultUserManager):
    """
    Custom user manager for handling user-related queries.
    
    This class extends Django's default `UserManager` and provides additional methods 
    for querying users based on various attributes such as ID, email, first name, last name, role, etc.
    """

    # getter for just 1 element
    def get_by_id(self, user_id):
        """
        Get a single user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user object matching the given ID.
        """
        return self.get(id=user_id)

    def get_by_email(self, email):
        """
        Get a single user by their email (unique).

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User: The user object matching the given email.
        """
        return self.get(email=email)

    # getter for multiple elements
    def get_by_first_name(self, first_name):
        """
        Get users matching a first name.

        Args:
            first_name (str): The first name to search for.

        Returns:
            QuerySet: A queryset containing users with the given first name.
        """
        return self.filter(first_name__icontains=first_name)

    def get_by_last_name(self, last_name):
        """
        Get users matching a last name.

        Args:
            last_name (str): The last name to search for.

        Returns:
            QuerySet: A queryset containing users with the given last name.
        """
        return self.filter(last_name__icontains=last_name)

    def get_by_role(self, role):
        """
        Get all users with a specific role.

        Args:
            role (str): The role to filter by.

        Returns:
            QuerySet: A queryset containing users with the given role.
        """
        return self.filter(role=role)

    def get_by_created_at(self, date):
        """
        Get users created on a specific date.

        Args:
            date (datetime.date): The date to filter by.

        Returns:
            QuerySet: A queryset containing users created on the given date.
        """
        return self.filter(created_at__date=date)

    def get_by_email_verify(self, is_verified: bool):
        """
        Get users filtered by email verification status.

        Args:
            is_verified (bool): The email verification status to filter by.

        Returns:
            QuerySet: A queryset containing users with the given email verification status.
        """
        return self.filter(email_verify=bool(is_verified))

    def get_by_a2f(self, a2f: bool):
        """
        Get users filtered by 2FA activation status.

        Args:
            a2f (bool): The 2FA activation status to filter by.

        Returns:
            QuerySet: A queryset containing users with the given 2FA activation status.
        """
        return self.filter(a2f=bool(a2f))

    def get_all(self):
        """
        Get all users.

        Returns:
            QuerySet: A queryset containing all users.
        """
        return self.all()

    def get_verified(self):
        """
        Get users who have verified their email.

        Returns:
            QuerySet: A queryset containing users with a verified email.
        """
        return self.filter(email_verify=True)

    def get_with_a2f_enabled(self):
        """
        Get users who have 2FA enabled.

        Returns:
            QuerySet: A queryset containing users with 2FA enabled.
        """
        return self.filter(a2f=True)

    def search(self, first_name=None, last_name=None, role=None, email_verify=None, a2f=None):
        """
        Dynamic search with optional filters.

        Args:
            first_name (str, optional): The first name to filter by.
            last_name (str, optional): The last name to filter by.
            role (str, optional): The role to filter by.
            email_verify (bool, optional): The email verification status to filter by.
            a2f (bool, optional): The 2FA activation status to filter by.

        Returns:
            QuerySet: A queryset containing users matching the provided filters.
        """
        search = self.all()
        if first_name:
            search = search.filter(first_name__icontains=first_name)
        if last_name:
            search = search.filter(last_name__icontains=last_name)
        if role:
            search = search.filter(role=role)
        if email_verify is not None:
            search = search.filter(email_verify=bool(email_verify))
        if a2f is not None:
            search = search.filter(a2f=bool(a2f))
        return search