from django.db import models
from auth_app.managers.ItemsEDNManager import ItemsEDNManager

class ItemsEDN(models.Model):
    # Integer field for the item number, optional and can be null
    numero = models.IntegerField(blank=True, null=True, verbose_name="Numéro")

    # Character field for the item title, up to 500 characters long
    titre = models.CharField(max_length=500, verbose_name="Titre")

    # Character field for the writing college name, up to 500 characters long
    writing_college = models.CharField(max_length=500, verbose_name="Collège d'écriture")

    # Character field for the proofreading college name, up to 500 characters long
    proofreading_college = models.CharField(max_length=500, verbose_name="Collège de relecture")

    # Custom manager for this model
    objects = ItemsEDNManager()

    def __str__(self):
        # String representation of the model instance
        return f"Item EDN : {self.numero} : {self.titre}"

    class Meta:
        # Verbose name for a single object
        verbose_name = "Item EDN"
        # Verbose name for multiple objects
        verbose_name_plural = "Items EDN"