from django.db import models

class StartingSituation(models.Model):
    """
    Model representing the starting situation in a scenario or workflow.
    
    Attributes:
        groups_id (int, optional): ID of the group associated with this situation. 
            It is nullable and can be used to categorize situations under different groups.
        
        number_situation (int, optional): Unique identifier for this situation within the scenario.
            It ranges from 1 to 356 and is nullable.

        text_situation (str, optional): Detailed textual description of the starting situation. 
            This field can be used to provide additional context or details about the situation.
    """

    groups_id = models.IntegerField(verbose_name="ID du grand titre", null=True, blank=True)
    
    # Corresponds to the starting situation and its positions in the table
    number_situation = models.IntegerField(verbose_name="Numéro de la situation de départ 1/356", null=True, blank=True)
    
    text_situation = models.TextField(verbose_name="Texte de la situation de départ", null=True, blank=True)

    def __str__(self):
        return f"Situation {self.number_situation} : {self.text_situation}"