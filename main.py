import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(token=os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в MoneyBox!')


bot.polling(none_stop=True)