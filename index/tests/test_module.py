import pytest
from index.models import Comment
from django.contrib.auth.models import User

def test_comment_str(db):
    user = User.objects.create_user(username='ABOBA', password='12345password')
    com = Comment.objects.create(user=user, text='This is a test comment')
    
    assert com.text == 'This is a test comment'
    assert str(com) == 'ABOBA - This is a test comment - ' + str(com.created_at)
    assert com.user == user
    assert com.created_at is not None



