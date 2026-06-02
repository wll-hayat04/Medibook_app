from django.db import models

class ProfilPatient(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.TextField(blank=True)
    groupe_sanguin = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name_plural = "Profils patients"