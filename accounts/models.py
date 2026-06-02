from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('medecin', 'Médecin'),
        ('admin', 'Administrateur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def is_patient(self):
        return self.role == 'patient'

    def is_medecin(self):
        return self.role == 'medecin'

    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"