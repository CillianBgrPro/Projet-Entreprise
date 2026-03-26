from django.db import models

class TicketManager(models.Manager):
    def get_open_tickets(self):
        """Get open tickets."""
        return self.filter(status__iexact='open')
