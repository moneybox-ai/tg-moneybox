from telebot.util import quick_markup

from constants import callback_data


MENU = quick_markup({
    'кошельки': {'callback_data': callback_data.WALLETS_LIST},
    'переводы': {'callback_data': callback_data.TRANSFERS_LIST},
    'удалить токен': {'callback_data': callback_data.TOKEN_DELETE},
    'отмена': {'callback_data': callback_data.BACK_TO_START},
}, row_width=2)
TOKEN_ADD = quick_markup({
    'сохранить токен': {'callback_data': callback_data.TOKEN_ADD},
    'отмена': {'callback_data': callback_data.BACK_TO_START},
}, row_width=2)
TOKEN_DELETE = quick_markup({
    'удалить токен': {'callback_data': callback_data.TOKEN_TERMINATE},
    'отмена': {'callback_data': callback_data.BACK_TO_START},
}, row_width=2)
TO_START = quick_markup({
    'сохранить токен': {'callback_data': callback_data.TOKEN_ADD},
    'в начало': {'callback_data': callback_data.BACK_TO_START},
}, row_width=2)
