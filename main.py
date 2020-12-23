from shop.bot.shop_bot import bot, app_bot
import time
from shop.bot.config import WEBHOOK_URL
from shop.api.restful import app_rest

#bot.polling()
bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(WEBHOOK_URL, certificate=open('webhook_cert.pem'))
#app.run()

#app_rest.run(debug=True)