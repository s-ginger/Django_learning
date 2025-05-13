import pytest
from index.models import Comment, CustomUser, Course, Lesson

def test_comment_str(db):
    user = CustomUser.objects.create(username='testuser', password='testpass')
    comment = Comment.objects.create(user=user, text='This is a test comment')
    
    assert str(comment) == f"{user} - This is a test comment - {comment.created_at}"

def test_custom_user_str(db):
    user = CustomUser.objects.create(username='testuser', password='testpass', role='student', birth_date='2000-01-01')
    
    assert str(user) == f"{user.username} - {user.role} - {user.birth_date}"
    
def test_course_str(db):
    user = CustomUser.objects.create(username='testuser', password='testpass', role='teacher', birth_date='2000-01-01')
    course = Course.objects.create(title='Test Course', instructor=user, description='This is a test course')
    
    assert str(course) == 'Test Course'
    
def test_lesson_str(db):
    user = CustomUser.objects.create(username='testuser', password='testpass', role='teacher', birth_date='2000-01-01')
    course = Course.objects.create(title='Test Course', instructor=user, description='This is a test course')
    lesson = Lesson.objects.create(course=course, title='Test Lesson', content='This is a test lesson')
    
    assert str(lesson) == 'Test Lesson'



