from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from habits.models import Habit
from users.models import User
from .bot import TelegramBot
import logging

logger = logging.getLogger(__name__)
bot = TelegramBot()


@shared_task
def send_habit_reminders():
    """
    Отправка напоминаний о привычках.
    Запускается каждый час.
    """
    now = timezone.now()
    current_time = now.time()

    logger.info(f"Запуск отправки напоминаний на {now}")

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute__lte=current_time.minute + 30,
        user__telegram_chat_id__isnull=False
    ).select_related('user')

    sent_count = 0
    for habit in habits:
        last_reminder = habit.updated_at.date()
        days_since_last = (now.date() - last_reminder).days

        if days_since_last % habit.periodicity == 0:
            message = create_reminder_message(habit)
            result = bot.send_message(habit.user.telegram_chat_id, message)

            if result and result.get('ok'):
                sent_count += 1
                logger.info(f"Напоминание отправлено для привычки {habit.id}")
            else:
                logger.error(f"Ошибка отправки для привычки {habit.id}")

    logger.info(f"Отправлено {sent_count} напоминаний")
    return f"Отправлено {sent_count} напоминаний"


def create_reminder_message(habit):
    """Создание текста напоминания"""
    time_until = calculate_time_until(habit.time)

    message = f"<b>Напоминание о привычке</b>\n\n"
    message += f"<b>Действие:</b> {habit.action}\n"
    message += f"<b>Место:</b> {habit.place}\n"
    message += f"<b>Время:</b> {habit.time.strftime('%H:%M')}\n"
    message += f"<b>Длительность:</b> {habit.duration} секунд\n"

    if time_until > 0:
        message += f"<b>Осталось:</b> {time_until} минут\n\n"

    if habit.reward:
        message += f"<b>Награда после выполнения:</b> {habit.reward}\n"
    elif habit.related_habit:
        message += f"<b>После выполнения можно:</b> {habit.related_habit.action}\n"

    message += "\nУдачи в выполнении!"
    return message


def calculate_time_until(habit_time):
    """Расчет времени до выполнения привычки в минутах"""
    now = timezone.now()
    habit_datetime = timezone.make_aware(
        datetime.combine(now.date(), habit_time)
    )

    if habit_datetime < now:
        habit_datetime += timedelta(days=1)

    time_diff = habit_datetime - now
    return int(time_diff.total_seconds() / 60)


@shared_task
def send_test_notification(user_id, chat_id):
    """Отправка тестового уведомления"""
    try:
        message = "Это тестовое уведомление! Ваш бот работает правильно."
        result = bot.send_message(chat_id, message)
        return result
    except Exception as e:
        logger.error(f"Ошибка отправки тестового уведомления: {e}")
        return None


from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def test_celery():
    """Тестовая задача для проверки работы Celery"""
    logger.info("Celery работает правильно!")
    return "Celery task executed successfully"


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках"""
    from habits.models import Habit
    from datetime import datetime
    from .bot import TelegramBot

    bot = TelegramBot()
    current_time = datetime.now().time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__telegram_chat_id__isnull=False
    )

    sent_count = 0
    for habit in habits:
        message = f"Напоминание: {habit.action} в {habit.place}"
        result = bot.send_message(habit.user.telegram_chat_id, message)
        if result and result.get('ok'):
            sent_count += 1

    logger.info(f"Отправлено {sent_count} напоминаний")
    return f"Sent {sent_count} reminders"