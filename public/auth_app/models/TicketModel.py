from django.db import models
from auth_app.managers import TicketManager

class Ticket(models.Model):
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

class TicketReply(models.Model):
    """Réponse à un ticket."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies', verbose_name="Ticket")
    user = models.ForeignKey('auth_app.User', on_delete=models.CASCADE, related_name='ticket_replies', verbose_name="Auteur de la réponse")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de réponse")

    def __str__(self):
        return f"Réponse au ticket {self.ticket.id} par {self.user.username}"

    class Meta:
        verbose_name = "Réponse de Ticket"
        verbose_name_plural = "Réponses de Tickets"
        ordering = ['created_at']
