import json
from flask import Flask, request, abort
from mongoengine import NotUniqueError
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
                          InlineKeyboardButton, Message, Update, ReplyKeyboardRemove
from shop.models.shop_models import Category, User, Product, Cart, Order, News
from .config import TOKEN, WEBHOOK_URI
from .utils import inline_kb_from_iterable, inline_kb_from_dict
from . import constants

app = Flask(__name__)
bot = TeleBot(TOKEN)


@app.route(WEBHOOK_URI, methods=['POST'])
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
        print(products)
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
    cart = user.get_active_cart()
    is_product = cart.add_product(product)
    if not is_product:
        bot.answer_callback_query(
            call.id,
            'Продукт добавлен в корзину'
        )
    else:
        bot.answer_callback_query(
            call.id,
            'Продукт уже есть в корзине'
        )


@bot.message_handler(func=lambda m: constants.START_KB[constants.SETTINGS] == m.text)
def handle_settings(message: Message):
    user = User.objects.get(telegram_id=message.chat.id)
    data = user.formatted_data()
    kb = inline_kb_from_dict(constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(
        user.telegram_id,
        data,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.NAME_TAG)
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
    kb = inline_kb_from_dict(constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(message.chat.id, data, reply_markup=kb)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.PHONE_TAG)
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
    kb = inline_kb_from_dict(constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(message.chat.id, data, reply_markup=kb)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.EMAIL_TAG)
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
    kb = inline_kb_from_dict(constants.SETTINGS_KB, user.telegram_id)
    bot.send_message(message.chat.id, data, reply_markup=kb)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.ADDRESS_TAG)
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
    kb = inline_kb_from_dict(constants.SETTINGS_KB, user.telegram_id)
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
    user = User.objects.get(telegram_id=message.chat.id)
    cart = user.get_active_cart()
    count_products = len(cart.products)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = [KeyboardButton(n) for n in constants.ORDER_KB.values()]
    kb.add(*button)
    bot.send_message(message.chat.id, f'Ваш заказ ({count_products})', reply_markup=kb)
    if count_products == 0:
        text_message = 'Корзина пуста'
        bot.send_message(
            message.chat.id,
            text_message
        )
    else:
        id = cart.products[0].product.id
        product = Product.objects.get(id=id)
        count_product = cart.products[0].count
        price = product.product_price * count_product
        text_message = f'{product.title}, Количество - {count_product}, Цена {price}'
        kb = inline_kb_from_dict(constants.CART_KB, user.telegram_id)
        bot.send_message(
            message.chat.id,
            text_message,
            reply_markup=kb
        )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.NEXT_TAG)
def handle_next_product(call):
    telegram_id = json.loads(call.data)['id']
    user = User.objects.get(telegram_id=telegram_id)
    cart = user.get_active_cart()
    count_products = len(cart.products)
    status = cart.is_status
    if status < (count_products - 1):
        status += 1
        cart.update(is_status=status)
        id_ = cart.products[status].product.id
        product = Product.objects.get(id=id_)
        count_product = cart.products[status].count
        price = product.product_price * count_product
        kb = inline_kb_from_dict(constants.CART_KB, user.telegram_id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'{product.title}, Количество - {count_product}, Цена {price}',
            reply_markup=kb
        )
    else:
        bot.answer_callback_query(
            call.id,
            'Это последний'
        )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.PREVIOUS_TAG)
def handle_previous_product(call):
    user = User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_cart()
    status = cart.is_status
    if status > 0:
        status -= 1
        cart.update(is_status=status)
        id_ = cart.products[status].product.id
        product = Product.objects.get(id=id_)
        count_product = cart.products[status].count
        price = product.product_price * count_product
        kb = inline_kb_from_dict(constants.CART_KB, user.telegram_id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'{product.title}, Количество - {count_product}, Цена {price}',
            reply_markup=kb
        )
    else:
        bot.answer_callback_query(
            call.id,
            'Это первый'
        )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.INCREASE_TAG)
def handle_increase_product(call):
    telegram_id = json.loads(call.data)['id']
    user = User.objects.get(telegram_id=telegram_id)
    cart = user.get_active_cart()
    status = cart.is_status
    product = cart.products[status]
    product.count += 1
    cart.save()
    price = product.price * product.count
    kb = inline_kb_from_dict(constants.CART_KB, user.telegram_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f'{product.title}, Количество - {product.count}, Цена {price}',
        reply_markup=kb
    )


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.REDUCE_TAG)
def handle_reduce_product(call):
    telegram_id = json.loads(call.data)['id']
    user = User.objects.get(telegram_id=telegram_id)
    cart = user.get_active_cart()
    status = cart.is_status
    product = cart.products[status]
    product.count -= 1
    cart.save()
    price = product.price * product.count
    for p in cart.products:
        if p.count == 0:
            cart.products.remove(p)
            cart.save()
    if len(cart.products) == 0:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'Корзина пуста',
        )
    else:
        kb = inline_kb_from_dict(constants.CART_KB, user.telegram_id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'{product.title}, Количество - {product.count}, Цена {price}',
            reply_markup=kb
        )


@bot.message_handler(func=lambda m: constants.ORDER_KB[constants.RETURN_START] == m.text)
def handler_return(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in constants.START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, 'вы вернулись в главное меню', reply_markup=kb)


@bot.message_handler(func=lambda m: constants.ORDER_KB[constants.FINISH] == m.text)
def handler_finish(message: Message):
    user = User.objects.get(telegram_id=message.chat.id)
    cart = user.get_active_cart()
    count = cart.total_count()
    price = cart.total_price()
    number = len(Order.objects())
    order = Order(user=user, number=number + 1, cart=cart, total_count=count, total_price=price)
    order.save()
    cart.is_active = False
    cart.save()
    bot.send_message(message.chat.id, constants.NAME_TEXT, reply_markup=ReplyKeyboardRemove())
    user.modify(is_status_order=constants.FIRST_NAME)


@bot.message_handler(func=lambda message: User.get_is_order(message.chat.id) == constants.FIRST_NAME)
def order_entering_name(message):
    text = f'"{message.text}"'
    user = User.objects.get(telegram_id=message.chat.id)
    order = user.get_active_order()
    order.user_name = text
    order.save()
    bot.send_message(message.chat.id, constants.PHONE_TEXT)
    user.modify(is_status_order=constants.PHONE)


@bot.message_handler(func=lambda message: User.get_is_order(message.chat.id) == constants.PHONE)
def order_entering_phone(message):
    text = f'"{message.text}"'
    user = User.objects.get(telegram_id=message.chat.id)
    order = user.get_active_order()
    order.phone = text
    order.save()
    bot.send_message(message.chat.id, constants.EMAIL_TEXT)
    user.modify(is_status_order=constants.EMAIL)


@bot.message_handler(func=lambda message: User.get_is_order(message.chat.id) == constants.EMAIL)
def order_entering_email(message):
    text = f'{message.text}'
    user = User.objects.get(telegram_id=message.chat.id)
    order = user.get_active_order()
    order.email = text
    order.save()
    bot.send_message(message.chat.id, constants.ADDRESS_TEXT)
    user.modify(is_status_order=constants.ADDRESS)


@bot.message_handler(func=lambda message: User.get_is_order(message.chat.id) == constants.ADDRESS)
def order_entering_address(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(constants.CONFIRM)
    kb.add(button)
    text = f'"{message.text}"'
    user = User.objects.get(telegram_id=message.chat.id)
    order = user.get_active_order()
    order.address = text
    order.save()
    cart = order.cart
    products = ''
    for p in cart.products:
        products += f'{p}\n'
    products += f'Всего товаров - {order.total_count}\nК оплате - {order.total_price}\n'
    text = f'Заказ № {order.number}\n\n{products}\n\nФИО - {order.user_name}\n' \
           f'телефон - {order.phone}\nemail - {order.email}\nадрес - {order.address}'
    bot.send_message(message.chat.id, text, reply_markup=kb)
    user.modify(is_status_order=0)


@bot.message_handler(func=lambda m: m.text == constants.CONFIRM)
def handle_confirm(message: Message):
    user = User.objects.get(telegram_id=message.chat.id)
    order = user.get_active_order()
    order.is_active = False
    order.save()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in constants.START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, constants.THANKS, reply_markup=kb)
