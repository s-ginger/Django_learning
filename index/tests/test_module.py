import pytest
from django.utils import timezone
from index.models import CustomUser, Course, Lesson, Comment, CommentCourse, Question, Answer, Test, LessonProgress

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



@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        username="testuser",
        password="testpassword",
        role="student",
        birth_date="2000-01-01"
    )

@pytest.fixture
def instructor():
    return CustomUser.objects.create_user(
        username="instructor",
        password="instructorpassword",
        role="teacher",
        birth_date="1980-01-01"
    )

@pytest.fixture
def course(instructor):
    return Course.objects.create(
        title="Test Course",
        instructor=instructor,
        description="A test course"
    )

@pytest.fixture
def lesson(course):
    return Lesson.objects.create(
        course=course,
        title="Test Lesson",
        content="Lesson content",
    )

@pytest.fixture
def comment(user, lesson):
    return Comment.objects.create(
        user=user,
        text="Test comment",
        created_at=timezone.now()
    )

@pytest.fixture
def test(course):
    return Test.objects.create(
        course=course,
        title="Test Title",
        description="Test description"
    )

@pytest.fixture
def question(test):
    return Question.objects.create(
        test=test,
        text="What is the answer?"
    )

@pytest.fixture
def answer(question):
    return Answer.objects.create(
        question=question,
        text="This is a correct answer",
        is_correct=True
    )


def test_custom_user_creation(user):
    assert user.username == "testuser"
    assert user.role == "student"
    assert user.birth_date == "2000-01-01"


def test_course_creation(course, instructor):
    assert course.title == "Test Course"
    assert course.instructor == instructor
    assert course.description == "A test course"


def test_lesson_creation(lesson, course):
    assert lesson.title == "Test Lesson"
    assert lesson.course == course
    assert lesson.content == "Lesson content"


def test_comment_creation(comment, user, lesson):
    assert comment.user == user
    assert comment.text == "Test comment"
    assert comment.lesson == lesson


def test_string_representation_of_comment(comment):
    expected_string = f"{comment.user} - {comment.text} - {comment.created_at}"
    assert str(comment) == expected_string


def test_lesson_progress_creation(user, lesson):
    progress = LessonProgress.objects.create(user=user, lesson=lesson, is_read=True)
    assert progress.user == user
    assert progress.lesson == lesson
    assert progress.is_read is True


def test_unique_together_of_lesson_progress(user, lesson):
    LessonProgress.objects.create(user=user, lesson=lesson, is_read=True)
    with pytest.raises(Exception):  # Expecting an integrity error because of unique_together constraint
        LessonProgress.objects.create(user=user, lesson=lesson, is_read=False)


def test_comment_course_creation(user, lesson):
    comment_course = CommentCourse.objects.create(
        user=user,
        lesson=lesson,
        content="Great lesson!"
    )
    assert comment_course.user == user
    assert comment_course.lesson == lesson
    assert comment_course.content == "Great lesson!"


def test_test_creation(test, course):
    assert test.title == "Test Title"
    assert test.course == course
    assert test.description == "Test description"


def test_question_creation(question, test):
    assert question.text == "What is the answer?"
    assert question.test == test


def test_answer_creation(answer, question):
    assert answer.text == "This is a correct answer"
    assert answer.is_correct is True
    assert answer.question == question


def test_string_representation_of_answer(answer):
    assert str(answer) == "This is a correct answer (Correct)"
