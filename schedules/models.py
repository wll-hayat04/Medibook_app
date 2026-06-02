from django.db import models
from doctors.models import Medecin

class Disponibilite(models.Model):
    JOURS = (
        (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'),
        (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche'),
    )
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='disponibilites')
    jour = models.IntegerField(choices=JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree_rdv = models.IntegerField(default=30, help_text="Durée en minutes")
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.medecin} - {self.get_jour_display()}"

    class Meta:
        verbose_name_plural = "Disponibilités"