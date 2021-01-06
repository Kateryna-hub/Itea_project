from shop.bot.shop_bot import bot, app
from shop.api.restful import app_rest
import time
from shop.bot.config import WEBHOOK_URL
from shop.models.shop_models import Category, Product, Parameters, News

#bot.polling()
# bot.remove_webhook()
# time.sleep(0.5)
# bot.set_webhook(WEBHOOK_URL, certificate=open('webhook_cert.pem'))
#app.run()
#app_rest.run()


news = {
    'news1': {
        'title': 'Готовимся к праздникам вместе',
        'body': 'У нас вы сможете купить подарки на любой вкус.'
    },
    'news2': {
        'title': 'Плати комфортно',
        'body': 'Теперь в нашем магазине вы можете оплачивать покупки через чат-бота.'
    },
    'news3': {
        'title': 'Экспрес доставка',
        'body': 'Мы запустили экспресс-доставку, которая гарантирует получение онлайн-заказа в течение двух часов'
    },
    'news4': {
        'title': 'Открытие филиала Харькове',
        'body': 'Мы расширяемся. Уже в этом году откроется новый склад-магазин в Харькове'
    },
    'news5': {
        'title': 'С новым годом!',
        'body': 'Большая новогодняя распродажа стартовала',
    }
}

#app_rest.run()

# import mongoengine as me
# from mongoengine import connect
#
# db = connect('SHOP')
# db.drop_database('SHOP')


root1 = (Category(title='Бытовая техника')). save()
category_fridges = (Category(title='Холодильники')). save()
category_fridge_bosch = (Category(title='Bosch')).save()
category_fridge_samsung = (Category(title='Samsung')).save()


category_wm = (Category(title='Стиральные машины')). save()
category_wm_ind = (Category(title='Indesit')).save()
category_wm_lg = (Category(title='LG')).save()


category_mw = (Category(title='Микроволновые печи')).save()
category_mw_bosch = (Category(title='Bosch')).save()
category_mw_samsung = (Category(title='Samsung')).save()

root1.add_subcategory(category_fridges)
category_fridges.add_subcategory(category_fridge_bosch)
category_fridges.add_subcategory(category_fridge_samsung)

root1.add_subcategory(category_wm)
category_wm.add_subcategory(category_wm_ind)
category_wm.add_subcategory(category_wm_lg)

root1.add_subcategory(category_mw)
category_mw.add_subcategory(category_mw_bosch)
category_mw.add_subcategory(category_mw_samsung)


root2 = (Category(title='Игрушки')). save()
category_soft_toys = (Category(title='Мягкие игрушки')).save()
category_constructors = (Category(title='Конструкторы')).save()
root2.add_subcategory(category_soft_toys)
root2.add_subcategory(category_constructors)


root3 = (Category(title='Товары для дома')). save()
category_dishes = (Category(title='Посуда')).save()
category_plates = (Category(title='Тарелки')).save()
category_pans = (Category(title='Кастрюли')).save()
category_textiles = (Category(title='Текстиль')).save()
category_bedding = (Category(title='Постельное белье')).save()
category_towels = (Category(title='Полотенца')).save()

root3.add_subcategory(category_dishes)
category_dishes.add_subcategory(category_plates)
category_dishes.add_subcategory(category_pans)


root3.add_subcategory(category_textiles)
category_textiles.add_subcategory(category_bedding)
category_textiles.add_subcategory(category_towels)


products = {
    'products1': {
        'title': 'Bosch KGN36NL306',
        'description': 'Двухкамерный; морозильная камера - снизу; цвет - серебро',
        'discount': 5,
        'price': 13299,
        'image': './image/bosch_f1.jpg',
        'category': category_fridge_bosch,
        'height': 186,
        'width': 60,
        'weight': 64,
        'additional_description': 'Технология NoFrost; Электронная регулировка температуры со светодиодной индикацией;'
                                  ' Функция быстрого замораживания SuperFreezing с автоматическим отключением'
    },
    'products2': {
        'title': 'BOSCH KGN49LB30U',
        'description': 'Двухкамерный; морозильная камера - снизу; Цвет - темно-серый Metallic Сhrome',
        'discount': 0,
        'price': 37199,
        'image': './image/bosch_f2.jpg',
        'category': category_fridge_bosch,
        'height': 203,
        'width': 70,
        'weight': 101,
        'additional_description': 'Функция быстрого охлаждения Super Сooling, функция быстрого замораживания '
                                  'SuperFreezing с автоматическим отключением, звуковой сигнал открытых дверей, '
                                  'Система охлаждения MultiAirflow, Фильтр очистки воздуха AirFreshfilter'
    },
    'products3': {
        'title': 'SAMSUNG RT46K6340S8/UA',
        'description': 'Двухкамерный; морозильная камера - сверху; Цвет - серебро',
        'discount': 0,
        'price': 19999,
        'image': './image/WM_LG.jpg',
        'category': category_fridge_samsung,
        'height': 182.5,
        'width': 70,
        'weight': 74,
        'additional_description': 'Многопоточная система Multi Flow, Двойная система охлаждения Twin Cooling, '
                                  'Система VoltControl, Внутренняя LED подсветка, Дезодоратор'
    },
    'products4': {
        'title': 'LG FH0J3NDN0',
        'description': 'автоматическая; Максимальная загрузка - 6 кг; 11 режимов стирки; 1000 об/мин',
        'discount': 10,
        'price': 10699.00,
        'image': './image/WM_LG.jpg',
        'category': category_wm_lg,
        'height': 85,
        'width': 60,
        'weight': 64,
        'additional_description': 'глубина 44, цвет - белый'
    },
    'products5': {
        'title': 'INDESIT IWSC 51051',
        'description': 'автоматическая; Максимальная загрузка - 5 кг; 16 режимов стирки; 1000 об/мин',
        'discount': 5,
        'price': 5449.00,
        'image': 'image/wm_indesit.jpg',
        'category': category_wm_ind,
        'height': 85,
        'width': 59.5,
        'weight': 62,
        'additional_description': 'глубина 42, цвет - белый'
    },
    'products6': {
        'title': 'INDESIT IWSC 51052A',
        'description': 'автоматическая; Максимальная загрузка - 5 кг; 11 режимов стирки; 1000 об/мин',
        'discount': 10,
        'price': 5800.00,
        'image': './image/wm_indesit2.jpg',
        'category': category_wm_ind,
        'height': 85,
        'width': 59.5,
        'weight': 64,
        'additional_description': 'глубина 42, цвет - белый'
    },
    'products7': {
        'title': 'SAMSUNG MG23F302TAS',
        'description': '41 программа автоприготовления; цвет - Серебристый',
        'discount': 10,
        'price': 3399.00,
        'image': './image/mw_samsung.jpg',
        'category': category_mw_samsung,
        'height': 27.54,
        'width': 48.9,
        'weight': 13,
        'additional_description': 'Поворотный стеклянный столик, Решетка для гриля'
    },
    'products8': {
        'title': 'SAMSUNG GE88SUB/BW',
        'description': '41 программа автоприготовления; цвет - Черный',
        'discount': 0,
        'price': 3499.00,
        'image': 'image/mw_samsung2.jpg',
        'category': category_mw_samsung,
        'height': 27.5,
        'width': 48.9,
        'weight': 15,
        'additional_description': 'Быстрый старт, Eco mode (режим сохранения энергии в режиме stand-by)'
    },
    'products9': {
        'title': 'BOSCH HMT72M450',
        'description': 'Поворотный стеклянный столик, Решетка для гриля, цвет - Нержавеющая сталь',
        'discount': 0,
        'price': 2699.00,
        'image': './image/mw_BOSCH_HMT72M450.jpg',
        'category': category_mw_bosch,
        'height': 33.5,
        'width': 51.2,
        'weight': 10,
        'additional_description': 'Быстрый старт, Eco mode (режим сохранения энергии в режиме stand-by)'
    },
    'products10': {
        'title': 'Мишка',
        'description': 'Плюшевый мишка',
        'discount': 5,
        'price': 245.00,
        'image': './image/bear.jpg',
        'category': category_soft_toys,
        'height': 45,
        'width': 20,
        'weight': 0.24,
        'additional_description': 'цвет-капучино'
    },
    'products11': {
        'title': 'LEGO Classic',
        'description': 'Модели из кубиков 123 детали',
        'discount': 22,
        'price': 363.00,
        'image': './image/lego.jpg',
        'category': category_constructors,
        'height': 14.1,
        'width': 6.1,
        'weight': 0.55,
        'additional_description': 'Набор включает в себя кубики, глаза, колёса и петли LEGO'
    },
    'products12': {
        'title': 'Bambi LT2003',
        'description': 'Магнитный конструктор, 97 деталей ',
        'discount': 10,
        'price': 756.00,
        'image': './image/magnet.jpg',
        'category': category_constructors,
        'height': 45.5,
        'width': 32,
        'weight': 0.4,
        'additional_description': 'Тема набора - Животные'
    },
    'products13': {
        'title': 'Тарелка суповая',
        'description': 'La Cucina 18 cм Black',
        'discount': 0,
        'price': 89.00,
        'image': './image/plate.jpg',
        'category': category_plates,
        'height': 1.5,
        'width': 18,
        'weight': 0.14,
        'additional_description': 'Керамика, круглая'
    },
    'products14': {
        'title': 'Кастрюля Ardesto Gemini',
        'description': 'Материал: Нержавеющая сталь, Диаметр 20 см',
        'discount': 0,
        'price': 399,
        'image': './image/pan.jpg',
        'category': category_pans,
        'height': 10,
        'width': 20,
        'weight': 1.4,
        'additional_description': 'Крышка - Стеклянная, Толщина дна 2.5 мм, для всех видов плит'
    },
    'products15': {
        'title': 'Комплект постельного белья',
        'description': 'Двуспальный, Бязь 19-2491 Leone 175х210',
        'discount': 10,
        'price': 1077.00,
        'image': './image/bed1.jpg',
        'category': category_bedding,
        'height': 15,
        'width': 35,
        'weight': 0.25,
        'additional_description': 'Пододеяльник 175 x 210 см - 1 шт, '
                                  'простынь 200 x 220 см - 1 шт, наволочка 50 x 70 см - 2 шт'
    },
    'products16': {
        'title': 'Комплект постельного белья',
        'description': 'Двуспальный, Бязь 116-5803 Geronimo 200х220',
        'discount': 10,
        'price': 1077.00,
        'image': './image/bed2.jpg',
        'category': category_bedding,
        'height': 15,
        'width': 35,
        'weight': 0.25,
        'additional_description': 'Пододеяльник 175 x 210 см - 1 шт, '
                                  'простынь 200 x 220 см - 1 шт, наволочка 50 x 70 см - 2 шт'
    },
    'products17': {
        'title': 'Полотенце махровое',
        'description': 'Style 500" плотность 500 гр/м2 100% хлопок',
        'discount': 0,
        'price': 480.00,
        'image': './image/towels2.jpg',
        'category': category_towels,
        'height': 70,
        'width': 140,
        'weight': 0.350,
        'additional_description': 'Изделие не теряет своего вида и формы даже после многих стирок'
    },
    'products18': {
        'title': 'Полотенце махровое',
        'description': 'Style 500" плотность 500 гр/м2 100% хлопок',
        'discount': 0,
        'price': 250.00,
        'image': './image/towels2.jpg',
        'category': category_towels,
        'height': 30,
        'width': 70,
        'weight': 0.150,
        'additional_description': 'Изделие не теряет своего вида и формы даже после многих стирок'
    }
    }

for p in products:
    pr = Parameters(height=products[p]['height'], width=products[p]['width'],
                    weight=products[p]['weight'], additional_description=products[p]['additional_description'])
    file = open(products[p]['image'], 'rb')
    product = (Product(title=products[p]['title'], description=products[p]['description'],
                       discount=products[p]['discount'], price=products[p]['price'],
                       category=products[p]['category'])).save()

    product.image.put(file, content_type='image/jpg')
    product.parameters = pr
    product.save()

for n in news:
    News(title=news[n]['title'], body=news[n]['body']).save()


