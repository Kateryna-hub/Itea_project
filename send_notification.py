from shop.bot.sending_news import Sender
from shop.models.shop_models import User


s = Sender(User.objects(), text='Рассылка')

s.send_message()