import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from telegram.bot import TelegramBot


class Command(BaseCommand):
    help = "Установка вебхука для Telegram бота"

    def add_arguments(self, parser):
        parser.add_argument("webhook_url", type=str, help="URL для вебхука")

    def handle(self, *args, **options):
        webhook_url = options["webhook_url"]
        bot = TelegramBot()

        # Сначала удаляем старый вебхук
        bot.delete_webhook()

        # Устанавливаем новый
        result = bot.set_webhook(webhook_url)

        if result and result.get("ok"):
            self.stdout.write(
                self.style.SUCCESS(f"Вебхук успешно установлен на {webhook_url}")
            )
        else:
            self.stdout.write(self.style.ERROR("Ошибка установки вебхука"))
