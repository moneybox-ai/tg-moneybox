import os

import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(token=os.getenv('TOKEN'))