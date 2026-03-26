from django.db import models
from auth_app.managers import TicketManager

class Ticket(models.Model):
    """Ticket de support."""
    user = models.ForeignKey('auth_app.User', on_delete=models.CASCADE, related_name='tickets', verbose_name="Utilisateur")
    subject = models.CharField(max_length=150, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    status = models.CharField(max_length=20, blank=True, verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    objects = TicketManager()

    def __str__(self):
        return f"[{self.status}] {self.subject}"

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
