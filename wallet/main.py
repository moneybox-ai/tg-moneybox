import telebot

from config import TELEGRAM_TOKEN

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в MoneyBox!')


bot.polling(none_stop=True)
