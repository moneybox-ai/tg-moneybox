from config import *


bot = telebot.TeleBot(token=os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в MoneyBox!')


bot.polling(none_stop=True)