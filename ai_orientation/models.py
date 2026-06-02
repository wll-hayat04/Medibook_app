from django.conf import settings
from django.db import models

class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nom
    
class Medecin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medecin_ai'
    )
    specialite = models.ForeignKey(
        Specialite,
        on_delete=models.CASCADE,
        related_name='medecins_ai'  # <-- nom unique pour cet app
    )
    telephone = models.CharField(max_length=20)