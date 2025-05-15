"""
URL configuration for mydjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from index.views import ( 
    main_page, 
    logins, 
    register, 
    about, 
    contact, 
    logout_view, 
    chat,
    courses_view,create_lesson, 
    course_lessons_view,lesson_detail_view,
    profile_view,profile,
    lesson_read
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', profile, name='profile'),
    path('', main_page, name='main'),
    path('courses/', courses_view, name='courses'),
    path('login/', logins, name='login'),
    path('logout/', logout_view, name='logout'),
    path('chat/', chat, name='chat'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('create_lesson/', create_lesson, name='create_lesson'),
    path('lesson/<int:lesson_id>/', lesson_detail_view, name='lesson_detail'),
    path('course/<int:course_id>/lessons/', course_lessons_view, name='course_lessons'),  # Страница с уроками курса
    path('profile/', profile_view, name='profile'),  # Страница профиля
    path('isreadles/<int:lesson_id>', lesson_read, name='isreadles'),  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
