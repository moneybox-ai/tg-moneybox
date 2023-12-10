from telebot import types


class Button:
    ADD_EXPENSE = types.KeyboardButton('➕ Добавить расход')
    LIST_EXPENSE = types.KeyboardButton('💸 Список расходов')


class Message:
    ADD_EXPENSE = '➕ Добавить расход'
    LIST_EXPENSE = '💸 Список расходов'
    WELCOME_TO_MONEYBOX = 'Добро пожаловать в MoneyBox!'
    ADD_AMOUNT = 'Введите сумму расхода:'
    EXPENSES = 'Расходы:'
