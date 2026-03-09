import json
import logging
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from habits.models import Habit

from .bot import TelegramBot, get_bot_commands

logger = logging.getLogger(__name__)
User = get_user_model()
bot = TelegramBot()


@csrf_exempt
def telegram_webhook(request):
    """Обработка входящих сообщений от Telegram"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"Получено сообщение: {data}")

            # Обработка сообщений
            if "message" in data:
                handle_message(data["message"])
            elif "callback_query" in data:
                handle_callback(data["callback_query"])

            return JsonResponse({"ok": True})
        except Exception as e:
            logger.error(f"Ошибка обработки вебхука: {e}")
            return JsonResponse({"ok": False, "error": str(e)})

    return JsonResponse({"ok": False, "error": "Method not allowed"})


def handle_message(message):
    """Обработка текстовых сообщений"""
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/"):
        handle_command(chat_id, text, message)
    else:
        handle_regular_message(chat_id, text, message)


def handle_command(chat_id, command, message):
    """Обработка команд бота"""
    command = command.lower().split("@")[0]

    if command == "/start":
        send_welcome_message(chat_id, message)
    elif command == "/help":
        send_help_message(chat_id)
    elif command == "/my_habits":
        send_today_habits(chat_id, message)
    elif command == "/tomorrow":
        send_tomorrow_habits(chat_id, message)
    elif command == "/connect":
        send_connect_instructions(chat_id)
    else:
        bot.send_message(
            chat_id, "Неизвестная команда. Напишите /help для списка команд."
        )


def send_welcome_message(chat_id, message):
    """Отправка приветственного сообщения"""
    from_user = message.get("from", {})
    username = from_user.get("first_name", "Пользователь")

    welcome_text = f"""
Привет, {username}!

Я бот для отслеживания полезных привычек. Помогу тебе не забывать о важных делах и формировать полезные привычки.

<b>Основные команды:</b>
/start - Начать работу
/help - Показать справку
/my_habits - Мои привычки на сегодня
/tomorrow - Привычки на завтра
/connect - Подключить аккаунт

Я буду присылать тебе напоминания о привычках в указанное время.
"""
    bot.send_message(chat_id, welcome_text)


def send_help_message(chat_id):
    """Отправка справочного сообщения"""
    help_text = """
<b>Справка по использованию бота</b>

<b>Команды:</b>
• /start - Начать работу с ботом
• /help - Показать это сообщение
• /my_habits - Список привычек на сегодня
• /tomorrow - Список привычек на завтра
• /connect - Подключить Telegram к аккаунту

<b>Как подключить аккаунт:</b>
1. Войдите в веб-приложение
2. В профиле найдите ваш Telegram ID
3. Отправьте команду /connect и следуйте инструкциям

<b>Уведомления:</b>
Бот будет автоматически присылать напоминания о привычках в указанное вами время.
"""
    bot.send_message(chat_id, help_text)


def send_connect_instructions(chat_id):
    """Инструкция по подключению аккаунта"""

    instructions = f"""
<b>Подключение аккаунта</b>

Для подключения Telegram к вашему аккаунту:

1. Откройте веб-приложение Habit Tracker
2. Перейдите в настройки профиля
3. Введите ваш Telegram Chat ID: <code>{chat_id}</code>
4. Сохраните изменения

После этого вы будете получать уведомления о привычках прямо в Telegram!
"""
    bot.send_message(chat_id, instructions)


def send_today_habits(chat_id, message):
    """Отправка привычек на сегодня"""
    telegram_username = message.get("from", {}).get("username")

    try:
        user = User.objects.get(telegram_username=telegram_username)

        today = timezone.now().date()
        habits = Habit.objects.filter(user=user, created_at__date=today)

        if habits.exists():
            habits_text = "<b>Ваши привычки на сегодня:</b>\n\n"
            for habit in habits:
                habits_text += f"{habit.time.strftime('%H:%M')} - {habit.action}\n"
                habits_text += f"{habit.place}\n"
                if habit.reward:
                    habits_text += f"Награда: {habit.reward}\n"
                habits_text += "\n"
        else:
            habits_text = "На сегодня нет запланированных привычек."

        bot.send_message(chat_id, habits_text)

    except User.DoesNotExist:
        bot.send_message(
            chat_id,
            """
Ваш Telegram не привязан к аккаунту.

Используйте команду /connect для получения инструкций по подключению.
        """,
        )


def send_tomorrow_habits(chat_id, message):
    """Отправка привычек на завтра"""
    telegram_username = message.get("from", {}).get("username")

    try:
        user = User.objects.get(telegram_username=telegram_username)

        tomorrow = timezone.now().date() + timedelta(days=1)
        habits = Habit.objects.filter(user=user, created_at__date=tomorrow)

        if habits.exists():
            habits_text = "<b>Ваши привычки на завтра:</b>\n\n"
            for habit in habits:
                habits_text += f"{habit.time.strftime('%H:%M')} - {habit.action}\n"
                habits_text += f"{habit.place}\n\n"
        else:
            habits_text = "На завтра нет запланированных привычек."

        bot.send_message(chat_id, habits_text)

    except User.DoesNotExist:
        bot.send_message(chat_id, "Аккаунт не подключен. Используйте /connect")


def handle_regular_message(chat_id, text, message):
    """Обработка обычных текстовых сообщений"""
    response = """
Я понимаю только команды. Напишите /help для списка доступных команд.
    """
    bot.send_message(chat_id, response)
