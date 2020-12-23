import json
from flask import Flask, request, abort
from mongoengine import NotUniqueError
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
                          InlineKeyboardButton, Message, Update


from ..models.shop_models import Category, User, Product, Cart, Order
from ..models.extra_models import News
from .config import TOKEN, WEBHOOK_URI
from .utils import inline_kb_from_iterable, inline_kb_from_list
from . import constants

app_bot = Flask(__name__)
bot = TeleBot(TOKEN)


@app_bot.route(WEBHOOK_URI, methods=['POST'])
def handle_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    abort(403)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        User.objects.create(
            telegram_id=message.chat.id,
            username=getattr(message.from_user, 'username', None),
            first_name=getattr(message.from_user, 'first_name', None)
        )
    except NotUniqueError:
        greetings = 'Рады видеть тебя снова с нашем Интернет магазине'
    else:
        name = f', {message.from_user.first_name}' if getattr(message.from_user, 'first_name') else ''
        greetings = constants.GREETINGS.format(name)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in constants.START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, greetings, reply_markup=kb)


@bot.message_handler(func=lambda m: constants.START_KB[constants.CATEGORIES] == m.text)
def handle_categories(message: Message):
    root_categories = Category.get_root_categories()
    kb = inline_kb_from_iterable(constants.CATEGORY_TAG, root_categories)
    bot.send_message(
        message.chat.id,
        'Выберите категорию',
        reply_markup=kb
    )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.CATEGORY_TAG)
def handle_category_click(call):
    category = Category.objects.get(
        id=json.loads(call.data)['id']
    )

    if category.subcategories:
        kb = inline_kb_from_iterable(constants.CATEGORY_TAG, category.subcategories)
        bot.edit_message_text(
            category.title,
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=kb

        )

    else:
        products = category.get_products()
        for p in products:
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text=constants.ADD_TO_CART,
                callback_data=json.dumps(
                    {
                        'id': str(p.id),
                        'tag': constants.PRODUCT_TAG
                    }
                )
            )
            kb.add(button)
            description = p.description if p.description else ''
            price = p.product_price
            bot.send_photo(
                call.message.chat.id,
                p.image.read(),
                caption=f'{p.title}\n\n{description}\n{p.parameters}\n\nЦена - {price} грн',
                reply_markup=kb
            )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.PRODUCT_TAG or
                            json.loads(c.data)['tag'] == constants.PRODUCTS_WITH_DISCOUNT_TAG)
def handle_add_to_cart(call):
    product_id = json.loads(call.data)['id']
    product = Product.objects.get(id=product_id)
    user = User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_card()
    cart.add_product(product)
    bot.answer_callback_query(
        call.id,
        'Продукт добавлен в корзину'
    )


@bot.message_handler(func=lambda m: constants.START_KB[constants.SETTINGS] == m.text)
def handle_settings(message: Message):
    user = User.objects.get(telegram_id=message.chat.id)
    data = user.formatted_data()
    kb = inline_kb_from_list(constants.SETTING_TAG, constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(
        user.telegram_id,
        data,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.SETTING_TAG)
def handle_change_name(call):
    telegram_id = json.loads(call.data)['id']
    user = User.objects.get(telegram_id=telegram_id)
    user.modify(is_status_change=constants.FIRST_NAME)
    bot.send_message(
        call.message.chat.id,
        'Напишите имя'
    )


@bot.message_handler(func=lambda message: User.get_status_change(message.chat.id) == constants.FIRST_NAME)
def user_entering_name(message):
    first_name = f'{message.text}'
    user = User.objects.get(telegram_id=message.chat.id)
    user.modify(is_status_change=0, first_name=first_name)
    data = user.formatted_data()
    kb = inline_kb_from_list(constants.SETTING_TAG, constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(message.chat.id, data, reply_markup=kb)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.SETTING_TAG)
def handle_change_phone(call):
    telegram_id = json.loads(call.data)['id']
    user = User.objects.get(telegram_id=telegram_id)
    user.modify(is_status_change=constants.PHONE)
    bot.send_message(
        call.message.chat.id,
        'Напишите телефон'
    )


@bot.message_handler(func=lambda message: User.get_status_change(message.chat.id) == constants.PHONE)
def user_entering_phone(message):
    phone = f'{message.text}'
    user = User.objects.get(telegram_id=message.chat.id)
    user.modify(is_status_change=0, phone=phone)
    data = user.formatted_data()
    kb = inline_kb_from_list(constants.SETTING_TAG, constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(message.chat.id, data, reply_markup=kb)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.SETTING_TAG)
def handle_change_email(call):
    telegram_id = json.loads(call.data)['id']
    user = User.objects.get(telegram_id=telegram_id)
    user.modify(is_status_change=constants.EMAIL)
    bot.send_message(
        call.message.chat.id,
        'Напишите email'
    )


@bot.message_handler(func=lambda message: User.get_status_change(message.chat.id) == constants.EMAIL)
def user_entering_email(message):
    email = f'{message.text}'
    user = User.objects.get(telegram_id=message.chat.id)
    user.modify(is_status_change=0, email=email)
    data = user.formatted_data()
    kb = inline_kb_from_list(constants.SETTING_TAG, constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(message.chat.id, data, reply_markup=kb)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.SETTING_TAG)
def handle_change_address(call):
    telegram_id = json.loads(call.data)['id']
    user = User.objects.get(telegram_id=telegram_id)
    user.modify(is_status_change=constants.ADDRESS)
    bot.send_message(
        call.message.chat.id,
        'Напишите адрес'
    )


@bot.message_handler(func=lambda message: User.get_status_change(message.chat.id) == constants.ADDRESS)
def user_entering_address(message):
    address = f'{message.text}'
    user = User.objects.get(telegram_id=message.chat.id)
    user.modify(is_status_change=0, address=address)
    data = user.formatted_data()
    kb = inline_kb_from_list(constants.SETTING_TAG, constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(message.chat.id, data, reply_markup=kb)


@bot.message_handler(func=lambda m: constants.START_KB[constants.NEWS] == m.text)
def handle_news(message: Message):
    news = News.objects.skip(News.objects.count() - 5)
    for n in news:
        show_news = f' {n.title}\n{n.body}'
        bot.send_message(
            message.chat.id,
            show_news
        )


@bot.message_handler(func=lambda m: constants.START_KB[constants.PRODUCTS_WITH_DISCOUNT] == m.text)
def handle_discount(message: Message):
    products = Product.objects(discount__ne=0)
    for p in products:
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(
            text=constants.ADD_TO_CART,
            callback_data=json.dumps(
                {
                    'id': str(p.id),
                    'tag': constants.PRODUCTS_WITH_DISCOUNT_TAG
                }
            )
        )
        kb.add(button)
        description = p.description if p.description else ''
        price = p.product_price
        bot.send_photo(
            message.chat.id,
            p.image.read(),
            caption=f'{p.title}\nСкидка - {p.discount}%\n{description}\n{p.parameters}\n'
                    f'\nЦена со скидкой - {price} грн',
            reply_markup=kb
        )


@bot.message_handler(func=lambda m: constants.START_KB[constants.CART] == m.text)
def handle_cart(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = [KeyboardButton(n) for n in constants.ORDER_KB.values()]
    kb.add(*button)
    bot.send_message(message.chat.id, 'Ваш заказ', reply_markup=kb)
    cart = Cart.objects.get(user=message.chat.id)
    for p in cart.products:
        ikb = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(
            text='+',
            callback_data=json.dumps(
                {
                    'title': p.title,
                    'tag': constants.CART_TAG
                }
            )
        )
        button2 = InlineKeyboardButton(
            text='-',
            callback_data=json.dumps(
                {
                    'title': p.title,
                    'tag': constants.CART_TAG
                }
            )
        )
        kb.add(button1, button2)
        bot.send_message(
            message.chat.id,
            f'{p.title}\nКоличество - {p.count}\nЦена -{p.price}',
            reply_markup=ikb
        )


@bot.message_handler(func=lambda m: constants.ORDER_KB[constants.CONTINUE] == m.text)
def handler_continue(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in constants.START_KB.values()]
    kb.add(*buttons)
    root_categories = Category.get_root_categories()
    kbi = inline_kb_from_iterable(constants.CATEGORY_TAG, root_categories)
    bot.send_message(
        message.chat.id,
        'Выберите категорию',
        reply_markup=kbi
    )

    bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=kb)




# @bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.CART_TAG)
# def handle_increase_number_of_product(call):
#     telegram_id = json.loads(call.data)['id']
#     user = User.objects.get(telegram_id=telegram_id)
#     user.modify(is_status_change=constants.FIRST_NAME)
#     bot.send_message(
#         call.message.chat.id,
#         'Напишите имя'
#     )
#
# @bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.CART_TAG)
# def handle_reduce_number_of_product(call):
#     telegram_id = json.loads(call.data)['id']
#     user = User.objects.get(telegram_id=telegram_id)
#     user.modify(is_status_change=constants.FIRST_NAME)
#     bot.send_message(
#         call.message.chat.id,
#         'Напишите имя'
#     )