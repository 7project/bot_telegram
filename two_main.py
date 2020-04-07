import telebot
import logging
from config import *
from telebot import apihelper
from datetime import datetime
from covid.api import CovId19Data

api = CovId19Data(force=False)

log = logging.getLogger('telebot')
log.setLevel(logging.INFO)
fh = logging.FileHandler("/var/log/tg_telebot.log", 'a', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    res = api.get_stats()
    send_text = f'<b>Время запуска скрипта - {datetime.now()}</b>' \
                f'<b>Статистика обнавлена - {res["last_updated"]}\n\n' \
                f'<b>В мире подтверждено - {res["confirmed"]}</b>' \
                f'<b>В мире погибло - {res["deaths"]}</b>'

    bot.send_message(message.chat.id, send_text, parse_mode='html')

    log.info(f'Called bot.. name: {message.from_user.first_name}, command: /test')

while True:
    try:
        bot.polling(none_stop=True)
        break
    except Exception as e:
        log.exception(f'Exception bot.. message: {e}.')
