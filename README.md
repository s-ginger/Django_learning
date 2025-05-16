# 🎓 Django Education Platform

Веб-приложение для онлайн-обучения, созданное на Django 5.1. Преподаватели могут создавать курсы и уроки, а студенты — проходить их, оставлять комментарии и отслеживать прогресс.

---

## 📌 Возможности

- 🔐 Регистрация и аутентификация пользователей
- 👤 Кастомная модель пользователя с ролями: student, teacher, admin
- 🧑‍🏫 Учителя могут создавать курсы и уроки
- 📚 Студенты могут изучать курсы, проходить уроки и оставлять комментарии
- 🗂 Прогресс уроков (прочитан/не прочитан)
- 🧪 Тесты с вопросами и ответами
- 💬 Общий чат
- 🖼 Загрузка изображений для уроков и аватаров

---

## ⚙️ Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## 🚀 Подготовка и запуск

### 2. Нужно принять миграции

```bash 
python manage.py makemigrations
python manage.py migrate
```

### 3. Вам нужно будет сделать свой .env в корне проекта файл указав туда все необходимое


### 4. Запуск сервера 

```bash
python manage.py runserver
```

# URL Configuration for mydjango Project

### 1. `/admin/`
- **View**: Admin site
- **Path**: `admin.site.urls`
- **Description**: Административный интерфейс Django.

### 2. `/tests/`
- **View**: `tests_view`
- **Path**: `tests_view`
- **Description**: Страница для тестов.

### 3. `/profile/`
- **View**: `profile`
- **Path**: `profile`
- **Description**: Страница профиля пользователя.

### 4. `/`
- **View**: `main_page`
- **Path**: `main_page`
- **Description**: Главная страница сайта.

### 5. `/courses/`
- **View**: `courses_view`
- **Path**: `courses_view`
- **Description**: Страница с курсами.

### 6. `/login/`
- **View**: `logins`
- **Path**: `logins`
- **Description**: Страница для входа в систему.

### 7. `/logout/`
- **View**: `logout_view`
- **Path**: `logout_view`
- **Description**: Страница для выхода из системы.

### 8. `/chat/`
- **View**: `chat`
- **Path**: `chat`
- **Description**: Страница чата.

### 9. `/register/`
- **View**: `register`
- **Path**: `register`
- **Description**: Страница регистрации.

### 10. `/about/`
- **View**: `about`
- **Path**: `about`
- **Description**: Страница "О нас".

### 11. `/contact/`
- **View**: `contact`
- **Path**: `contact`
- **Description**: Страница с контактной информацией.

### 12. `/create_lesson/`
- **View**: `create_lesson`
- **Path**: `create_lesson`
- **Description**: Страница для создания нового урока.

### 13. `/lesson/<int:lesson_id>/`
- **View**: `lesson_detail_view`
- **Path**: `lesson_detail_view`
- **Description**: Страница с деталями урока, где `<int:lesson_id>` — это ID урока.

### 14. `/course/<int:course_id>/lessons/`
- **View**: `course_lessons_view`
- **Path**: `course_lessons_view`
- **Description**: Страница с уроками курса, где `<int:course_id>` — это ID курса.

### 15. `/isreadles/<int:lesson_id>/`
- **View**: `lesson_read`
- **Path**: `lesson_read`
- **Description**: Страница для пометки урока как прочитанного, где `<int:lesson_id>` — это ID урока.

### 16. `/profile/`
- **View**: `profile_view`
- **Path**: `profile_view`
- **Description**: Страница профиля пользователя (возможно, это дублирует `/profile/`).

### Static and Media Files
- **Static Files Path**: `static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)`
- **Media Files Path**: `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`


