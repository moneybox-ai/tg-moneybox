import os

import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(token=os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def get_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Добавить расход')
    btn2 = types.KeyboardButton('Список расходов')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Добро пожаловать в MoneyBox!', reply_markup=markup)


@bot.message_handler(func=lambda message:True)
def handle_message(message):
    if message.text == 'Добавить расход':
        bot.send_message(message.chat.id, 'Введите сумму расхода:')

        bot.register_next_step_handler(message, process_amount_step)
    elif message.text == 'Список расходов': #добавлю сюда логику для сохранения расходов, после коннекта с БД
        
        bot.send_message(message.chat.id, 'Расходы:')

def process_amount_step(message):
    try:
        amount = float(message.text)
        bot.send_message(message.chat.id, f'Расход в размере {amount} успешно добавлен.')
    except ValueError:
        bot.send_message(message.chat.id, f'Неверная сумма расхода.')

bot.infinity_polling()