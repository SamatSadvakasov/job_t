from django.db import models
from django.contrib.auth.models import AbstractUser

TYPE_CHOICES = (
    ('1', 'Phone'),
    ('2', 'Email'),
)

class User(AbstractUser):
    type_id: str = models.CharField(
        max_length=1, choices=TYPE_CHOICES, verbose_name='Type ID', default='1')
