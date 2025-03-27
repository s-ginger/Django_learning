from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

#class CommentForm(forms.Form):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    comment = forms.CharField(max_length=150, required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
  


