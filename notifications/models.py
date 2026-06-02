from django.db import models
from accounts.models import CustomUser

class Notification(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif pour {self.utilisateur} - {self.message[:30]}"

    class Meta:
        ordering = ['-date_creation']