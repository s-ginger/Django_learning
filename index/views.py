from django.shortcuts import render, redirect
from .forms import CustomUserForm, LoginForm, CommentForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import Comment

# Create your views here.
def main_page(request):
    username = request.session.get('username')
    print(username)
    if username:
        user = User.objects.get(username=username)
        return render(request, 'index/mainpage.html', {'user': user})
    else:
        return render(request, 'index/mainpage.html', {'user': None})

def logout(request):
    del request.session['username']
    return redirect('main')

def logins(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                request.session['username'] = user.username
                return redirect('main')
            else:
                form.add_error('username', 'Username or password is incorrect')
    form = LoginForm()
    return render(request, 'index/login.html', {'form': form})

@csrf_protect
def chat(request):
    form = CommentForm()
    comments = Comment.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated or request.session.get('username') == None:
                return redirect('register')
            
            user = request.user
            comment = Comment(user=user, text=form.cleaned_data.get('text'))
            comment.save()
            return redirect('chat')
        
    return render(request, 'index/chat.html', {'form': form, 'comment': comments})


def about(request):
    return render(request, 'index/about.html')

def contact(request):
    return render(request, 'index/about.html')

class Register(View):
    template_name = 'index/register.html'
    
    def get(self, request):
        form = CustomUserForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                user = form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
            else:
                form.add_error('password2', 'Password does not match')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            
            request.session['username'] = user.username
            
            return redirect('main')
            
        return render(request, self.template_name, {'form': form})



