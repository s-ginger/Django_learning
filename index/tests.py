from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Comment, CustomUser, Course, Lesson, LessonProgress, CommentCourse, Test, Question, Answer


class ModelsTestCase(TestCase):
    def setUp(self):
        # Создание пользователя
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            birth_date='2000-01-01',
            role='student'
        )
        self.teacher = get_user_model().objects.create_user(
            username='testteacher',
            password='testpassword',
            birth_date='1990-01-01',
            role='teacher'
        )

        # Создание курса
        self.course = Course.objects.create(
            title='Test Course',
            instructor=self.teacher,
            description='A test course'
        )

        # Создание урока
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            content='Lesson content',
        )

        # Создание теста
        self.test = Test.objects.create(
            course=self.course,
            title='Test Exam',
            description='A test exam'
        )

        # Создание вопроса для теста
        self.question = Question.objects.create(
            test=self.test,
            text='What is 2 + 2?'
        )

        # Создание правильного ответа
        self.answer = Answer.objects.create(
            question=self.question,
            text='4',
            is_correct=True
        )

    def test_create_user(self):
        """Проверка создания пользователя"""
        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'student')

    def test_create_course(self):
        """Проверка создания курса"""
        course = Course.objects.get(title='Test Course')
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.instructor.username, 'testteacher')

    def test_create_lesson(self):
        """Проверка создания урока"""
        lesson = Lesson.objects.get(title='Test Lesson')
        self.assertEqual(lesson.title, 'Test Lesson')
        self.assertEqual(lesson.course.title, 'Test Course')

    def test_create_comment(self):
        """Проверка создания комментария к уроку"""
        comment = CommentCourse.objects.create(
            user=self.user,
            lesson=self.lesson,
            content='Great lesson!'
        )
        self.assertEqual(comment.user.username, 'testuser')
        self.assertEqual(comment.lesson.title, 'Test Lesson')
        self.assertEqual(comment.content, 'Great lesson!')

    def test_create_lesson_progress(self):
        """Проверка создания прогресса по уроку"""
        progress = LessonProgress.objects.create(
            user=self.user,
            lesson=self.lesson,
            is_read=True
        )
        self.assertEqual(progress.user.username, 'testuser')
        self.assertEqual(progress.lesson.title, 'Test Lesson')
        self.assertTrue(progress.is_read)

    def test_create_test(self):
        """Проверка создания теста"""
        test = Test.objects.get(title='Test Exam')
        self.assertEqual(test.title, 'Test Exam')
        self.assertEqual(test.course.title, 'Test Course')

    def test_create_question(self):
        """Проверка создания вопроса"""
        question = Question.objects.get(text='What is 2 + 2?')
        self.assertEqual(question.text, 'What is 2 + 2?')
        self.assertEqual(question.test.title, 'Test Exam')

    def test_create_answer(self):
        """Проверка создания ответа"""
        answer = Answer.objects.get(text='4')
        self.assertEqual(answer.text, '4')
        self.assertTrue(answer.is_correct)

    def test_user_comment_to_course(self):
        """Проверка добавления комментария пользователем"""
        comment = Comment.objects.create(
            user=self.user,
            text='This is a comment'
        )
        self.assertEqual(comment.user.username, 'testuser')
        self.assertEqual(comment.text, 'This is a comment')

    def test_custom_user_role(self):
        """Проверка ролей кастомных пользователей"""
        self.assertEqual(self.user.role, 'student')
        self.assertEqual(self.teacher.role, 'teacher')

    def test_enroll_user_in_course(self):
        """Проверка записи студента на курс"""
        self.course.students.add(self.user)
        self.assertIn(self.user, self.course.students.all())

    def test_delete_course(self):
        """Проверка удаления курса"""
        course = self.course
        course.delete()
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(title='Test Course')

    def test_delete_user(self):
        """Проверка удаления пользователя"""
        user = self.user
        user.delete()
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(username='testuser')

    def test_unique_lesson_progress(self):
        """Проверка уникальности прогресса урока для одного пользователя"""
        LessonProgress.objects.create(user=self.user, lesson=self.lesson, is_read=True)
        with self.assertRaises(Exception):
            LessonProgress.objects.create(user=self.user, lesson=self.lesson, is_read=False)

    def test_str_method_in_comment(self):
        """Проверка метода __str__ в комментариях"""
        comment = Comment.objects.create(user=self.user, text='Test comment')
        self.assertEqual(str(comment), f"{self.user} - Test comment - {comment.created_at}")








# Запуск тестов
if __name__ == '__main__':
    TestCase.main()
