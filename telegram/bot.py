import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id, text, parse_mode='HTML'):
        """Отправка сообщения пользователю"""
        url = f"{self.api_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка отправки сообщения в Telegram: {e}")
            return None

    def set_webhook(self, webhook_url):
        """Установка вебхука для бота"""
        url = f"{self.api_url}/setWebhook"
        data = {'url': webhook_url}
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка установки вебхука: {e}")
            return None

    def delete_webhook(self):
        """Удаление вебхука"""
        url = f"{self.api_url}/deleteWebhook"
        try:
            response = requests.post(url, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка удаления вебхука: {e}")
            return None


def get_bot_commands():
    """Возвращает список команд бота"""
    return [
        {"command": "start", "description": "Начать работу с ботом"},
        {"command": "help", "description": "Показать справку"},
        {"command": "my_habits", "description": "Мои привычки на сегодня"},
        {"command": "tomorrow", "description": "Привычки на завтра"},
        {"command": "connect", "description": "Подключить аккаунт"},
    ]