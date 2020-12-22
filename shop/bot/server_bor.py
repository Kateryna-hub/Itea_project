from flask import Flask, request, abort
from telebot.types import Update
import config
from telebot import TeleBot


app = Flask(__name__)
bot = TeleBot(config.TOKEN)


@app.route(config.WEBHOOK_URI, methods=['POST'])
def handle_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data()
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    abort(403)


bot.set_webhook(config.WEBHOOK_URL)