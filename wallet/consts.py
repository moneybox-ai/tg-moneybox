from telebot import types


class Button:
    ADD_EXPENSE = types.KeyboardButton('➕ Добавить расход')
    LIST_EXPENSE = types.KeyboardButton('💸 Список расходов')
    LIST_CATEGORY = types.KeyboardButton('Список категорий')


class Message:
    ADD_EXPENSE = '➕ Добавить расход'
    LIST_EXPENSE = '💸 Список расходов'
    WELCOME_TO_MONEYBOX = 'Добро пожаловать в MoneyBox!'
    ADD_AMOUNT = 'Введите сумму расхода:'
    EXPENSES = 'Расходы:'
    NOT_EXPENSES = 'Неверная сумма расхода!'
    ADDED_EXPENSE = 'Расход добавлен!'
    LIST_CATEGORY = 'Список категорий'
    CATEGORIES = 'Категории:'

expense_url = "http://moneybox.ddns.net"
