from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    TYPE_CHOICES = (
        ('phone', 'Phone'),
        ('email', 'Email'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_type = models.CharField(choices=TYPE_CHOICES, max_length=5)

    def __str__(self):
        return f"{self.user.username} ({self.id_type})"