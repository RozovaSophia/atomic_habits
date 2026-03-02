# Habit Tracker - Трекер полезных привычек


Бэкенд-часть SPA веб-приложения для трекинга полезных привычек, основанного на книге Джеймса Клира "Атомные привычки". Проект позволяет создавать, отслеживать и получать напоминания о полезных привычках через Telegram.


## 🎯 О проекте

Проект реализует backend для трекера привычек с следующими возможностями:
- Создание полезных и приятных привычек
- Напоминания через Telegram
- Публичные и приватные привычки
- Валидация по правилам из книги "Атомные привычки"

##Функциональность

### Модель привычки включает:
- Место выполнения
- Время выполнения
- Действие
- Периодичность (от 1 до 7 дней)
- Время на выполнение (до 120 секунд)
- Вознаграждение или связанная приятная привычка
- Признак публичности

### Основные возможности:
- Регистрация и авторизация пользователей
- CRUD для привычек
- Список публичных привычек
- Пагинация (5 привычек на страницу)
- Telegram интеграция для напоминаний
- Валидация по правилам книги
- Документация API (Swagger/ReDoc)

## Технологии

amqp==5.3.1
asgiref==3.11.1
billiard==4.2.4
celery==5.6.2
certifi==2026.2.25
charset-normalizer==3.4.4
click==8.3.1
click-didyoumean==0.3.1
click-plugins==1.1.1.2
click-repl==0.3.0
colorama==0.4.6
coverage==7.13.4
cron-descriptor==1.4.5
Django==6.0.2
django-celery-beat==2.9.0
django-cors-headers==4.9.0
django-timezone-field==7.2.1
djangorestframework==3.16.1
drf-yasg==1.21.15
flake8==7.3.0
idna==3.11
inflection==0.5.1
iniconfig==2.3.0
kombu==5.6.2
mccabe==0.7.0
packaging==26.0
pillow==12.1.1
pluggy==1.6.0
prompt_toolkit==3.0.52
psycopg2-binary==2.9.11
pycodestyle==2.14.0
pyflakes==3.4.0
Pygments==2.19.2
pytest==9.0.2
pytest-cov==7.0.0
pytest-django==4.12.0
python-crontab==3.3.0
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
pytz==2025.2
PyYAML==6.0.3
redis==7.2.1
requests==2.32.5
six==1.17.0
sqlparse==0.5.5
tzdata==2025.3
tzlocal==5.3.1
uritemplate==4.2.0
urllib3==2.6.3
vine==5.1.0
wcwidth==0.6.0


## 📦 Установка

### Предварительные требования
- Python 
- Redis
- PostgreSQL (опционально)

