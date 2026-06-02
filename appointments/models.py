from django.db import models
from accounts.models import CustomUser
from doctors.models import Medecin, Specialite

class RendezVous(models.Model):
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
        ('absent', 'Absent'),
    )
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rendez_vous')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='rendez_vous')
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    notes_medecin = models.TextField(blank=True)

    def __str__(self):
        return f"RDV {self.patient} avec {self.medecin} le {self.date}"

    class Meta:
        verbose_name_plural = "Rendez-vous"
        ordering = ['-date', '-heure']


class Consultation(models.Model):
    rendez_vous = models.OneToOneField(
        RendezVous, on_delete=models.CASCADE, related_name='consultation'
    )
    resume = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation — {self.rendez_vous}"