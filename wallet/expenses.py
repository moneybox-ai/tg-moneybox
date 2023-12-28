from datetime import datetime

import telebot
from openapi_client.models import Expense
from telebot import types

from config import TELEGRAM_TOKEN, initialize_expenses_api
from consts import *

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def get_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(Button.ADD_EXPENSE, Button.LIST_EXPENSE, Button.LIST_CATEGORY)
    bot.send_message(message.chat.id, Message.WELCOME_TO_MONEYBOX, reply_markup=markup)


@bot.message_handler(func=lambda message:True)
def handle_message(message):
    if message.text == Message.ADD_EXPENSE:
        bot.send_message(message.chat.id, Message.ADD_AMOUNT)
        bot.register_next_step_handler(message, process_amount_step)
    elif message.text == Message.LIST_EXPENSE:
        expenses_api = initialize_expenses_api()
        expenses = expenses_api.expense_list_with_http_info()
        if expenses.status_code == 200:
             bot.send_message(message.chat.id, f'{Message.EXPENSES}{expenses.raw_data}')
    elif message.text == Message.LIST_CATEGORY:
        expenses_api = initialize_expenses_api()
        response = expenses_api.expensecategory_list_with_http_info()
        if response.status_code == 200:
            bot.send_message(message.chat.id, f'{Message.CATEGORIES}{response.raw_data}')


def process_amount_step(message):
    try:
        expenses_api = initialize_expenses_api()
        amount = str(message.text)
        expense = Expense(id=1, created_at=datetime.now(), updated_at=datetime.now(), amount=amount, category=1, created_by=1, wallet=1, group=1)
        response = expenses_api.expense_create_with_http_info(expense)
        if response.status_code == 201:
            bot.send_message(message.chat.id, Message.ADDED_EXPENSE)
    except ValueError:
        bot.send_message(message.chat.id, Message.NOT_EXPENSES)


bot.infinity_polling()
