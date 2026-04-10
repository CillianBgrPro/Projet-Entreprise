"""
TicketManager Module

This module contains a custom manager class, `TicketManager`, which extends Django's default `models.Manager`. The manager provides various methods to efficiently query the `Ticket` model.
"""

from django.db import models

class TicketManager(models.Manager):

    """
    Manager for ticket objects.
    """

    def get_by_id(self, ticket_id):
        """
        Get a single ticket by its ID.

        Args:
            ticket_id (int): The ID of the ticket to retrieve.

        Returns:
            Ticket: A single `Ticket` object if found, otherwise raises `DoesNotExist`.
        """
        return self.get(id=ticket_id)

    def get_by_user(self, user_id):
        """
        Get all tickets belonging to a specific user.

        Args:
            user_id (int): The ID of the user whose tickets should be retrieved.

        Returns:
            QuerySet[Ticket]: A queryset containing all `Ticket` objects associated with the specified user.
        """
        return self.filter(user_id=user_id)

    def get_by_subject(self, subject):
        """
        Get tickets matching a subject keyword.

        Args:
            subject (str): The keyword to search for in ticket subjects.

        Returns:
            QuerySet[Ticket]: A queryset containing `Ticket` objects whose subject contains the specified keyword.
        """
        return self.filter(subject__icontains=subject)

    def get_by_status(self, status):
        """
        Get tickets with a specific status.

        Args:
            status (str): The status of the tickets to retrieve. Case-insensitive match is used.

        Returns:
            QuerySet[Ticket]: A queryset containing `Ticket` objects with the specified status.
        """
        return self.filter(status__iexact=status)

    def get_by_created_at(self, date):
        """
        Get tickets created on a specific date.

        Args:
            date (datetime.date): The date to filter tickets by. Only tickets created on this date will be returned.

        Returns:
            QuerySet[Ticket]: A queryset containing `Ticket` objects created on the specified date.
        """
        return self.filter(created_at__date=date)

    def get_open(self):
        """
        Get all open tickets.

        Returns:
            QuerySet[Ticket]: A queryset containing all `Ticket` objects that are currently open (status 'open').
        """
        return self.filter(status__iexact='open')

    def get_closed(self):
        """
        Get all closed tickets.

        Returns:
            QuerySet[Ticket]: A queryset containing all `Ticket` objects that are currently closed (status 'closed').
        """
        return self.filter(status__iexact='closed')

    # dynamic search

    def search(self, user_id=None, subject=None, status=None, date_from=None, date_to=None, username=None, zero_replies=False):
        """
        Dynamic search with optional filters.

        Args:
            user_id (int, optional): Filter tickets by the user ID.
            subject (str, optional): Filter tickets by a keyword in the subject.
            status (str, optional): Filter tickets by their status. Case-insensitive match is used.
            date_from (datetime.date, optional): Filter tickets created on or after this date.
            date_to (datetime.date, optional): Filter tickets created on or before this date.
            username (str, optional): Filter tickets based on the user's username.
            zero_replies (bool, optional): Filter tickets that have no replies.

        Returns:
            QuerySet[Ticket]: A queryset containing `Ticket` objects that match all specified filters.
        """
        search = self.all()
        if user_id:
            search = search.filter(user_id=user_id)
        if username:
            search = search.filter(user__username__icontains=username)
        if subject:
            search = search.filter(subject__icontains=subject)
        if status:
            search = search.filter(status__iexact=status)
        if date_from:
            search = search.filter(created_at__date__gte=date_from)
        if date_to:
            search = search.filter(created_at__date__lte=date_to)
        if zero_replies:
            search = search.filter(replies__isnull=True)
        return search