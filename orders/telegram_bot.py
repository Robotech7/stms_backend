import telebot
from django.conf import settings

# Не разобрался еще как динамически получать chat_id
chat_id = '-1001377529595'

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, parse_mode=None)


def send_notification(text):
    try:
        bot.send_message(chat_id, text)
    except Exception as error:
        print(f'{type(error).__name__} - {list(error.args)}')
        pass
