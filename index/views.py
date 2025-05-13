from django.shortcuts import render, redirect
from .forms import CustomUserForm, LoginForm, CommentForm
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views import View
from django.contrib.auth.models import User
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def main_page(request):
    return render(request, 'index/mainpage.html', {'user': request.user if request.user.is_authenticated else None})

def courses_page(request):
    return render(request,'index/courses.html')
def logout_view(request):
    auth_logout(request)
    return redirect('main')


def logins(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, 'Username or password is incorrect')
    else:
        form = LoginForm()
    return render(request, 'index/login.html', {'form': form})


def chat(request):
    form = CommentForm()
    comments = Comment.objects.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return redirect('register')
            
            Comment.objects.create(user=request.user, text=form.cleaned_data['text'])
            return redirect('chat')
        
    return render(request, 'index/chat.html', {'form': form, 'comment': comments})


def about(request):
    return render(request, 'index/about.html')


def contact(request):
    return render(request, 'index/about.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем нового пользователя
            messages.success(request, f'Account created for {form.cleaned_data.get("username")}!')
            return redirect('login')  # Перенаправляем на страницу логина
        else:
            messages.error(request, 'There was an error with your registration form.')
    else:
        form = UserCreationForm()

    return render(request, 'index/register.html', {'form': form})
