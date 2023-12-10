import requests
import json
import telebot
from telebot import types

from config import TELEGRAM_TOKEN
from consts import *

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def get_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(Button.ADD_EXPENSE, Button.LIST_EXPENSE)
    bot.send_message(message.chat.id, Message.WELCOME_TO_MONEYBOX, reply_markup=markup)


@bot.message_handler(func=lambda message:True)
def handle_message(message):
    if message.text == Message.ADD_EXPENSE:
        bot.send_message(message.chat.id, Message.ADD_AMOUNT)
        bot.register_next_step_handler(message, process_amount_step)
    elif message.text == Message.LIST_EXPENSE:
        bot.send_message(message.chat.id, Message.EXPENSES)

def process_amount_step(message):
    try:
        amount = float(message.text)
        bot.send_message(message.chat.id, f'Расход в размере {amount} успешно добавлен.')
    except ValueError:
        bot.send_message(message.chat.id, f'Неверная сумма расхода.')

bot.infinity_polling()
