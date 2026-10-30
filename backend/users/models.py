from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, blank=True, null=True) # <-- Campo extra
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Email es el login, username requerido por defecto