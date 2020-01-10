import os

import telebot

from bot import TelegramBot
from flask import Flask, request, abort

from time import sleep

app = Flask(__name__)

# avoid 429 http error from telegram when sets webhook
sleep(3)

bot = TelegramBot(
    token=os.environ.get('telegram_token'),
    api_url=os.environ.get('api_url'),
    host=os.environ.get('host'),
    ssl_cert_path=os.environ.get('ssl_cert_path')
)


@app.route('/telegrambot/webhook/', methods=['POST'])
def webhook_handler():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@app.route('/sendMessage', methods=['POST'])
def send():
    if request.headers.get('content-type') == 'application/json':
        data = request.json
        bot.send_message(data['messenger_id'], data['text'])


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
