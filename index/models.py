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
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('user', 'User'), ('student', 'Student'), ('teacher', 'Teacher')], default='user')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=False)
    
    def __str__(self):
        return f"{self.username} - {self.role} - {self.birth_date}"
