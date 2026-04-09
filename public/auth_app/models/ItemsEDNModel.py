from django.db import models
from auth_app.managers.ItemsEDNManager import ItemsEDNManager

class ItemsEDN(models.Model):
    numero = models.IntegerField(blank=True, null=True, verbose_name="Numéro")
    titre = models.CharField(max_length=500, verbose_name="Titre")
    writing_college = models.CharField(max_length=500, verbose_name="Collège d'écriture")
    proofreading_college = models.CharField(max_length=500, verbose_name="Collège de relecture")

    objects = ItemsEDNManager()

    def __str__(self):
        return f"Item EDN : {self.numero} : {self.titre}"

    class Meta:
        verbose_name = "Item EDN"
        verbose_name_plural = "Items EDN"
