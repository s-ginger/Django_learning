from django.contrib import admin
from .models import Comment, CustomUser, Course, Lesson,CommentCourse

# Register your models here.
admin.site.register(Comment)
admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CommentCourse)