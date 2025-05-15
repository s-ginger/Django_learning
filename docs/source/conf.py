import os
import sys
import django

# Указываем путь до корня проекта (где manage.py)
sys.path.insert(0, os.path.abspath('..'))  # если conf.py в docs/

# Указываем модуль настроек Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'  # замените на ваш settings

# Инициализируем Django
django.setup()

# -- Project information -----------------------------------------------------

project = 'eduplatform'
copyright = '2025, Stepan && Samir'
author = 'Stepan && Samir'
release = '0.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.napoleon',       # если вы используете Google/NumPy-style docstrings
    # 'sphinx.ext.viewcode',       # добавляет ссылки на исходники
    # 'sphinx.ext.autosummary',    # создает автоматические резюме
]

autosummary_generate = True  # Чтобы создавались .rst автоматически
templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
