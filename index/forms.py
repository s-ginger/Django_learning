from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, CustomUser
from .models import Lesson, Course
from .models import CommentCourse
from django import forms
from .models import CommentCourse


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'image']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Ограничиваем выбор курсов только для тех, которые принадлежат учителю
            self.fields['course'].queryset = Course.objects.filter(instructor=user)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CustomUserForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Биография")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio')  # Поля для создания пользователя

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()  # Сохраняем пользователя
        return user


class CommentCourseForm(forms.ModelForm):
    class Meta:
        model = CommentCourse
        fields = ['content']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий...',
                'rows': 4
            })
        }


