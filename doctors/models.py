from django.db import models
from ai_orientation.models import Specialite
from django.conf import settings  # pour utiliser settings.AUTH_USER_MODEL si nécessaire
class Medecin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medecin_doctors'
    )
    specialite = models.ForeignKey(
        Specialite,
        on_delete=models.SET_NULL,
        null=True,
        related_name='medecins_doctors'  # <-- nom unique pour cet app
    )
    telephone = models.CharField(max_length=20, default="Non renseigné")
    
class Avis(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='avis')
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'medecin')
        ordering = ['-date_creation']

    def __str__(self):
        return f"Avis de {self.patient} sur {self.medecin} — {self.note}/5"