from django.db import models

class StartingSituation(models.Model):
    groups_id = models.IntegerField(verbose_name="ID du grand titre", null=True, blank=True)
    # Corresponnd au situation de départ et à leurs positions dans le tableau
    number_situation = models.IntegerField(verbose_name="Numéro de la situation de départ 1/356", null=True, blank=True)
    text_situation = models.TextField(verbose_name="Texte de la situation de départ", null=True, blank=True)

    def __str__(self):
        return f"Situation {self.number_situation} : {self.text_situation}"