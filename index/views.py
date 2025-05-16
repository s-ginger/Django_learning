from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from .models import (
    Course, 
    Lesson, 
    CommentCourse, 
    Comment, 
    Test, 
    Question, 
    Answer,
    LessonProgress
)

from .forms import (
    CustomUserForm, 
    LoginForm, 
    CommentForm, 
    CommentCourseForm, 
    LessonForm, 
    CourseForm, 
    TestForm, 
    QuestionForm, 
    AnswerForm
)



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
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('main')  # Можно перенаправить на профиль или главную страницу      
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
        return redirect('main')

    lesson_form = LessonForm(user=request.user)
    course_form = CourseForm()
    test_form = TestForm(user=request.user)
    QuestionFormSet = inlineformset_factory(Test, Question, form=QuestionForm, extra=1)
    question_formset = None
    answer_formset = None

    if request.method == 'POST':
        if 'create_course' in request.POST:
            course_form = CourseForm(request.POST, instructor=request.user)
            if course_form.is_valid():
                course_form.save()
                messages.success(request, "Course created successfully!")
                return redirect('create_lesson')

        elif 'create_lesson' in request.POST:
            lesson_form = LessonForm(request.POST, request.FILES, user=request.user)
            if lesson_form.is_valid():
                lesson = lesson_form.save(commit=False)
                lesson.course = lesson_form.cleaned_data['course']
                lesson.save()
                messages.success(request, "Lesson created successfully!")
                return redirect('course_lessons', course_id=lesson.course.id)

        elif 'create_test' in request.POST:
            test_form = TestForm(request.POST, user=request.user)
            if test_form.is_valid():
                test = test_form.save(commit=False)
                test.save()
                # Создаем formset для вопросов к этому тесту
                question_formset = QuestionFormSet(request.POST, instance=test)
                if question_formset.is_valid():
                    questions = question_formset.save(commit=False)
                    for question in questions:
                        question.test = test
                        question.save()
                    messages.success(request, "Test and questions created successfully!")
                    return redirect('create_lesson')
                else:
                    messages.error(request, "Error with questions formset")
            else:
                messages.error(request, "Error with test form")

    else:
        question_formset = QuestionFormSet()

    context = {
        'form': lesson_form,
        'course_form': course_form,
        'test_form': test_form,
        'question_formset': question_formset,
    }
    return render(request, 'index/create_lesson.html', context)


def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.user.is_authenticated:
        # Получаем или создаём прогресс
        progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

        # Обновляем статус на прочитано
        if not progress.is_read:
            progress.is_read = True
            progress.save()
            
        progress_dict = {}
    if request.user.is_authenticated:
        lessons = Lesson.objects.filter(course=lesson.course)  # ✅ ЭТОГО НЕ ХВАТАЛО
        progresses = LessonProgress.objects.filter(user=request.user, lesson__in=lessons)
        progress_dict = {p.lesson_id: p.is_read for p in progresses}

        
    print(f"Progress: {progress.is_read}")  
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
        'form': form,
        'progress_dict': progress_dict,
    }
    return render(request, 'index/lesson_detail.html', context)


def lesson_read(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    lesson_progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'is_read': True}
    )
    if not created:
        lesson_progress.is_read = True
    lesson_progress.save()
    
    next = lesson.course.lessons.filter(id__gt=lesson.id).first()
    if next:
        return redirect('lesson_detail', lesson_id=next.id)
    else:
        # Если это последний урок, можно перенаправить на курс или другую страницу
        return redirect('course_lessons', course_id=lesson.course.id)
    