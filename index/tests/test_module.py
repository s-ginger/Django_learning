import pytest
from django.utils import timezone
from index.models import CustomUser, Course, Lesson, Comment, CommentCourse, Question, Answer

@pytest.mark.django_db
def test_create_custom_user():
    user = CustomUser.objects.create_user(username='testuser', password='pass123', role='student', birth_date='2000-01-01')
    assert user.username == 'testuser'
    assert user.role == 'student'
    assert user.check_password('pass123')

@pytest.mark.django_db
def test_create_course():
    teacher = CustomUser.objects.create_user(username='teacher1', password='pass', role='teacher', birth_date='1980-01-01')
    course = Course.objects.create(title='Math', instructor=teacher, description='Basic math course')
    assert course.title == 'Math'
    assert course.instructor == teacher

@pytest.mark.django_db
def test_enroll_student():
    teacher = CustomUser.objects.create_user(username='teacher2', password='pass', role='teacher', birth_date='1980-01-01')
    student = CustomUser.objects.create_user(username='student1', password='pass', role='student', birth_date='2005-01-01')
    course = Course.objects.create(title='Science', instructor=teacher, description='Science course')
    course.students.add(student)
    assert student in course.students.all()

@pytest.mark.django_db
def test_create_lesson():
    teacher = CustomUser.objects.create_user(username='teacher3', password='pass', role='teacher', birth_date='1975-05-05')
    course = Course.objects.create(title='History', instructor=teacher, description='History course')
    lesson = Lesson.objects.create(course=course, title='Lesson 1', content='Intro to history')
    assert lesson.course == course
    assert lesson.title == 'Lesson 1'

@pytest.mark.django_db
def test_create_comment():
    user = CustomUser.objects.create_user(username='commenter', password='pass', role='user', birth_date='1990-06-15')
    comment = Comment.objects.create(user=user, text='This is a chat comment')
    assert comment.user == user
    assert comment.text == 'This is a chat comment'

@pytest.mark.django_db
def test_comment_course():
    teacher = CustomUser.objects.create_user(username='t1', password='pass', role='teacher', birth_date='1970-01-01')
    student = CustomUser.objects.create_user(username='s1', password='pass', role='student', birth_date='2004-09-01')
    course = Course.objects.create(title='Biology', instructor=teacher, description='Bio course')
    lesson = Lesson.objects.create(course=course, title='DNA', content='DNA basics')
    comment = CommentCourse.objects.create(user=student, lesson=lesson, content='Interesting topic!')
    assert comment.lesson == lesson
    assert comment.user == student

@pytest.mark.django_db
def test_question_and_answer():
    teacher = CustomUser.objects.create_user(username='t2', password='pass', role='teacher', birth_date='1985-03-03')
    course = Course.objects.create(title='Physics', instructor=teacher, description='Physics 101')
    lesson = Lesson.objects.create(course=course, title='Gravity', content='Gravity basics')
    question = Question.objects.create(lesson=lesson, text='What is gravity?')
    answer1 = Answer.objects.create(question=question, text='A force', is_correct=True)
    answer2 = Answer.objects.create(question=question, text='A color', is_correct=False)

    assert question.lesson == lesson
    assert answer1.question == question
    assert answer1.is_correct
    assert not answer2.is_correct
