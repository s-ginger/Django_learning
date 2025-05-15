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

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

    def __init__(self, *args, instructor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instructor = instructor

    def save(self, commit=True):
        course = super().save(commit=False)
        if self.instructor:
            course.instructor = self.instructor
        if commit:
            course.save()
        return course


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

from django import forms
from django.forms import inlineformset_factory
from .models import Test, Question, Answer
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'course']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(instructor=user)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

QuestionFormSet = inlineformset_factory(Test, Question, form=QuestionForm, extra=1)
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4)
