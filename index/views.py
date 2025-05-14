from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, CommentCourse, Comment
from .forms import CustomUserForm, LoginForm, CommentForm, CommentCourseForm, LessonForm
from django.shortcuts import get_object_or_404, redirect, render


def main_page(request):
    return render(request, 'index/mainpage.html', {'user': request.user if request.user.is_authenticated else None})

def courses_view(request):
    courses = Course.objects.all()  # Получаем все курсы из базы
    return render(request, 'index/courses.html', {'courses': courses})

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
    return render(request, 'index/logreg.html', {'form': form})

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
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем нового пользователя через кастомную форму
            messages.success(request, f'Account created for {form.cleaned_data.get("username")}!')
            return redirect('login')  # Перенаправляем на страницу логина
        else:
            messages.error(request, 'There was an error with your registration form.')
    else:
        form = CustomUserForm()

    return render(request, 'index/register.html', {'form': form})


def course_lessons_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Получаем курс по ID
    lessons = course.lessons.all()  # Получаем все уроки этого курса
    return render(request, 'index/courses_detail.html', {'course': course, 'lessons': lessons})


def profile_view(request):
    return render(request, 'index/cabinet.html', {'user': request.user})

def profile(request):
    return render(request, 'index/cabinet.html', {'user': request.user})
@login_required
def create_lesson(request):
    if request.user.role != 'teacher':
        return redirect('main')  # Если пользователь не учитель, перенаправляем на главную страницу

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, user=request.user)  # Передаем пользователя в форму
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = form.cleaned_data['course']
            lesson.save()
            return redirect('course_lessons', course_id=lesson.course.id)  # Перенаправляем на страницу курса
    else:
        form = LessonForm(user=request.user)  # Передаем пользователя при GET-запросе

    return render(request, 'index/create_lesson.html', {'form': form})


def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Получаем все уроки курса и находим следующий по id
    course_lessons = Lesson.objects.filter(course=lesson.course).order_by('id')
    next_lesson = course_lessons.filter(id__gt=lesson.id).first()

    # Комментарии к уроку
    comments = CommentCourse.objects.filter(lesson=lesson).order_by('-created_at')

    # Обработка формы комментариев
    form = CommentCourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.lesson = lesson
        comment.save()

    context = {
        'lesson': lesson,
        'next_lesson': next_lesson,
        'comments': comments,
        'form': form
    }
    return render(request, 'index/lesson_detail.html', context)