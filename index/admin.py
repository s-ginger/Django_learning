from django.contrib import admin
from .models import Comment, CustomUser, Course, Lesson,CommentCourse,Question,Test,Answer
# Register your models here.
admin.site.register(Comment)
admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CommentCourse)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(Answer)
