from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import  AbstractBaseUser
from mydjango.settings import AUTH_USER_MODEL

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user} - {self.text} - {self.created_at}"


class CustomUser(AbstractUser):
    address = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=False)
