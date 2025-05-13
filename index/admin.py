from django.contrib import admin
from .models import Comment, CustomUser

# Register your models here.
admin.site.register(Comment)
admin.site.register(CustomUser)