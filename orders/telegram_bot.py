import telebot
from django.conf import settings

chat_id = '-392778246'

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, parse_mode=None)


def send_notification(text):
    bot.send_message(chat_id, text)
