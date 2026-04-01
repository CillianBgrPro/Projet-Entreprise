from django.db import models

class TicketManager(models.Manager):

    # getter return 1 element

    def get_by_id(self, ticket_id):
        #Get a single ticket by its ID.
        return self.get(id=ticket_id)

    # getter return a list

    def get_by_user(self, user_id):
        #Get all tickets belonging to a specific user.
        return self.filter(user_id=user_id)

    def get_by_subject(self, subject):
        #Get tickets matching a subject keyword.
        return self.filter(subject__icontains=subject)

    def get_by_status(self, status):
        #Get tickets with a specific status.
        return self.filter(status__iexact=status)

    def get_by_created_at(self, date):
        #Get tickets created on a specific date.
        return self.filter(created_at__date=date)

    def get_open(self):
        #Get all open tickets.
        return self.filter(status__iexact='open')

    def get_closed(self):
        #Get all closed tickets.
        return self.filter(status__iexact='closed')

    # dynamic search

    def search(self, user_id=None, subject=None, status=None):
        #Dynamic search with optional filters.
        search = self.all()
        if user_id:
            search = search.filter(user_id=user_id)
        if subject:
            search = search.filter(subject__icontains=subject)
        if status:
            search = search.filter(status__iexact=status)
        return search
