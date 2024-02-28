import logging
from pprint import pprint

from telebot import TeleBot, types
from telebot.util import quick_markup
from openapi_client import WalletsApi

from config import bot_token

from constants import messages, callback_data
from constants.commands import START, HELP
from constants.keyboards import MENU, TOKEN_ADD, TOKEN_DELETE, TO_START

from servises.api import get_api, get_wallets, get_currency
from servises.validators import is_number
from servises.token_db import get_user_token, save_user_token, delete_user_token  # noqa


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_id(call):
    return int(call.data.split(':')[-1])


bot = TeleBot(bot_token)
logger.info('Бот успешно запущен.')


@bot.message_handler(commands=[START, HELP])
def send_welcome(message):
    text = None
    reply_markup = None
    try:
        user_token = get_user_token(message.chat.id)
        if user_token:
            reply_markup = MENU
            text = messages.WALLETS_START
        else:
            reply_markup = TOKEN_ADD
            text = messages.NO_TOKEN
    except Exception as e:
        logger.error(e, exc_info=True)
    if text and reply_markup:
        bot.send_message(message.chat.id, text, reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data == callback_data.TOKEN_DELETE)  # noqa
def delete_token(call):
    bot.send_message(call.message.chat.id, messages.CONFIRM_DELETE,
                     reply_markup=TOKEN_DELETE)


@bot.callback_query_handler(func=lambda call: call.data == callback_data.TOKEN_TERMINATE)  # noqa
def terminate_token(call):
    token = delete_user_token(call.message.chat.id)
    text = f'токен {token} удален!'
    bot.send_message(call.message.chat.id, text, reply_markup=TO_START)


@bot.callback_query_handler(func=lambda call: call.data == callback_data.TOKEN_ADD)  # noqa
def add_token(call):
    message = bot.send_message(call.message.chat.id, messages.ADD_TOKEN)
    bot.register_next_step_handler(message, save_token)


def save_token(message):
    try:
        save_user_token(message.from_user.id, message.text)
    except Exception as e:
        logger.error(e, exc_info=True)
    send_welcome(message)


@bot.callback_query_handler(func=lambda call: call.data == callback_data.BACK_TO_START)  # noqa
def back_to_start(call):
    send_welcome(call.message)


@bot.callback_query_handler(func=lambda call: call.data == callback_data.WALLETS_LIST)  # noqa
def wallets(call):
    token = get_user_token(call.message.chat.id).token
    wllts = get_wallets(token)
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 4
    row = []
    if len(wllts) > 0:
        for item in wllts:
            row.append(types.InlineKeyboardButton(
                f"{item.name} {item.balance}",
                callback_data=callback_data.WALLET_SHOW.format(item.id),
            ))
            if len(row) == markup.row_width:
                markup.add(*row)
                row = []
        markup.add(*row)
    markup.add(types.InlineKeyboardButton(
        "добавить кошелек",
        callback_data=callback_data.WALLET_ADD,
    ))
    markup.add(types.InlineKeyboardButton(
        "назад",
        callback_data=callback_data.BACK_TO_START,
    ))
    bot.send_message(call.message.chat.id, messages.CHOUSE_WALLET,
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(callback_data.WALLET_SHOW.format('')))  # noqa
def wallet_edit(call, **kwargs):
    id = get_id(call)
    token = get_user_token(call.message.chat.id).token
    wllts = get_wallets(token)
    for item in wllts:
        if item.id == id:
            message = item.to_str()
            break
        else:
            message = f'кошелек с ID {id} не найден'
    markup = quick_markup({
        'назад': {'callback_data': callback_data.WALLETS_LIST},
        'отмена': {'callback_data': callback_data.BACK_TO_START},
    }, row_width=2)
    bot.send_message(call.message.chat.id, message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == callback_data.WALLET_ADD)  # noqa
def wallet_add(call):
    token = get_user_token(call.message.chat.id).token
    currency = get_currency(token)
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 4
    row = []
    if len(currency) > 0:
        for item in currency:
            row.append(types.InlineKeyboardButton(
                f"{item.code}",
                callback_data=callback_data.CURRENCY_GET.format(item.id),
            ))
            if len(row) == markup.row_width:
                markup.add(*row)
                row = []
        markup.add(*row)
    markup.add(
        types.InlineKeyboardButton(
            "назад",
            callback_data=callback_data.WALLETS_LIST,
        ),
        types.InlineKeyboardButton(
            "отмена",
            callback_data=callback_data.BACK_TO_START,
        ),
    )
    bot.send_message(call.message.chat.id, messages.CHOUSE_CURRENCY,
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(callback_data.CURRENCY_GET.format('')))  # noqa
def wallet_add_currency(call):
    id = get_id(call)
    obj = {'currency': id}
    message = bot.send_message(call.message.chat.id, messages.BALLANSE_INPUT)
    bot.register_next_step_handler(message, wallet_add_balance, obj)


def wallet_add_balance(message, *args):
    obj = args[0]
    string = message.text.replace(',', '.').lower()
    if not is_number(string):
        message = bot.send_message(message.chat.id, messages.BALLANSE_INPUT)
        bot.register_next_step_handler(message, wallet_add_balance, obj)
    else:
        obj['balance'] = string
        message = bot.send_message(message.chat.id, messages.WALLET_NAME_INPUT)
        bot.register_next_step_handler(message, wallet_save, obj)


def wallet_save(message, *args):
    obj = args[0]
    string = message.text
    if string is None or len(string) < 2:
        message = bot.send_message(message.chat.id, messages.WALLET_NAME_INPUT)
        bot.register_next_step_handler(message, wallet_save, obj)
    else:
        obj['name'] = string
        obj["is_deleted"] = False
        token = get_user_token(message.chat.id).token
        api = get_api(WalletsApi, token)
        try:
            api.wallet_create(wallet=obj)
        except Exception as e:
            logger.error(e, exc_info=True)
        bot.send_message(message.chat.id, messages.ADD_WALLET_SUCSESS)


bot.infinity_polling()
