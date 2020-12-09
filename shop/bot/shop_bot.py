import json

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from ..models.shop_models import Category
from .config import TOKEN
from .utils import inline_kb_from_iterable
from . import constants

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    name = f', {message.from_user.first_name}' if getattr(message.from_user, 'first_name') else ''
    greetings = constants.GREETINGS.format(name)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in constants.START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, greetings, reply_markup=kb)


@bot.message_handler(func=lambda m: constants.START_KB[constants.CATEGORIES] == m.text)
def handle_categories(message):
    root_categories = Category.get_root_categories()
    kb = inline_kb_from_iterable(constants.CATEGORY_TAG, root_categories)
    bot.send_message(
        message.chat.id,
        'Выберите категорию',
        reply_markup=kb
    )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.CATEGORY_TAG)
def handle_category_click(call):
    print(call)

