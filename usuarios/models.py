from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    telefone = models.CharField(max_length = 20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.get_full_name() or self.username