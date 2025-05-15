from django.test import TestCase
from django.utils import timezone
from .models import CustomUser, Course, Lesson, Comment, CommentCourse, Question, Answer
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime


class ModelTests(TestCase):
    
    def setUp(self):
        # Создание пользователей
        self.teacher = CustomUser.objects.create_user(
            username='teacher1',
            password='pass1234',
            role='teacher',
            birth_date='1990-01-01'
        )
        self.student = CustomUser.objects.create_user(
            username='student1',
            password='pass1234',
            role='student',
            birth_date='2000-05-15'
        )

        # Создание курса
        self.course = Course.objects.create(
            title='Python Course',
            instructor=self.teacher,
            description='Learn Python from scratch'
        )
        self.course.students.add(self.student)

        # Создание урока
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Introduction',
            content='Welcome to the Python course!'
        )

        # Создание вопроса и ответа
        self.question = Question.objects.create(
            lesson=self.lesson,
            text='What is Python?'
        )
        self.answer = Answer.objects.create(
            question=self.question,
            text='A programming language',
            is_correct=True
        )

        # Комментарии
        self.chat_comment = Comment.objects.create(
            user=self.student,
            text='This course is great!',
            created_at=timezone.now()
        )

        self.lesson_comment = CommentCourse.objects.create(
            user=self.student,
            lesson=self.lesson,
            content='Nice lesson!'
        )

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(self.teacher.role, 'teacher')
        self.assertEqual(self.student.role, 'student')

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Python Course')
        self.assertEqual(self.course.instructor, self.teacher)
        self.assertIn(self.student, self.course.students.all())

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.title, 'Introduction')
        self.assertEqual(self.lesson.course, self.course)

    def test_question_and_answer(self):
        self.assertEqual(self.question.text, 'What is Python?')
        self.assertEqual(self.answer.question, self.question)
        self.assertTrue(self.answer.is_correct)

    def test_comment_models(self):
        self.assertEqual(self.chat_comment.text, 'This course is great!')
        self.assertEqual(self.lesson_comment.lesson, self.lesson)
        self.assertEqual(self.lesson_comment.user, self.student)

    def test_str_methods(self):
        self.assertIn('Python Course', str(self.course))
        self.assertIn('Introduction', str(self.lesson))
        self.assertIn('What is Python?', str(self.question))
        self.assertIn('A programming language', str(self.answer))
        self.assertIn('Комментарий от', str(self.lesson_comment))
        self.assertIn(self.student.username, str(self.chat_comment))
