from django.db import models
from auth_app.managers import TicketManager

class Ticket(models.Model):
    """
    Represents a support ticket in the system.

    Fields:
        user: A foreign key to the User model, linking the ticket to the user who created it.
        subject: A CharField for the subject of the ticket, with a maximum length of 150 characters.
        message: A TextField for the detailed message of the ticket.
        status: A CharField for the current status of the ticket, which can be blank.
        created_at: A DateTimeField that automatically records when the ticket was created.

    Relationships:
        - The Ticket model has a one-to-many relationship with the TicketReply model through the 'replies' field.
        - The Ticket model has a foreign key relationship with the User model through the 'user' field.

    Methods:
        __str__: Returns a string representation of the ticket in the format "[Status] Subject".
    """

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
    """
    Represents a reply to a support ticket.

    Fields:
        ticket: A foreign key to the Ticket model, linking the reply to its associated ticket.
        user: A foreign key to the User model, linking the reply to the user who created it.
        message: A TextField for the text of the reply.
        created_at: A DateTimeField that automatically records when the reply was created.

    Relationships:
        - The TicketReply model has a one-to-many relationship with itself through the 'replies' field.
        - The TicketReply model has a foreign key relationship with the User model through the 'user' field.

    Methods:
        __str__: Returns a string representation of the reply in the format "Response to ticket {Ticket ID} by {User Username}".
    """

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