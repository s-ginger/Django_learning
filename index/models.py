from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from mydjango.settings import AUTH_USER_MODEL

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user} - {self.text} - {self.created_at}"


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=[('teacher', 'Teacher'), ('student', 'Student')], default='student')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        return f"{self.first_name} {self.last_name}"

