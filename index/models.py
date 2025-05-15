from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import  AbstractBaseUser
from mydjango.settings import AUTH_USER_MODEL

# Create your models here.
class Comment(models.Model):
    '''Класс для комментариев в чате'''
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user} - {self.text} - {self.created_at}"


class CustomUser(AbstractUser):
    '''Класс для кастомной модели пользователя'''
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('user', 'User'), ('student', 'Student'), ('teacher', 'Teacher')], default='student')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=False)
    
    def __str__(self):
        return f"{self.username} - {self.role} - {self.birth_date}"


class Course(models.Model):
    '''Класс для курсов'''
    title = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='courses',
        limit_choices_to={'role': 'teacher'} 
        )
    
    students = models.ManyToManyField(
        CustomUser, 
        related_name='enrolled_courses', 
        blank=True,
        limit_choices_to={'role': 'student'}
        )
    
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    '''Класс для уроков'''
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    isRead = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class CommentCourse(models.Model):
    '''Класс для комментариев к курсам'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.user.username} к {self.lesson.title}'

class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"
