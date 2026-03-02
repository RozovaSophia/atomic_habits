from celery.loaders import app
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-habit-reminders': {
        'task': 'telegram.tasks.send_habit_reminders',
        'schedule': crontab(minute='*/30'),  # Каждые 30 минут
    },
}