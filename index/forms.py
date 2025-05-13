from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, CustomUser

User = get_user_model()

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
