import telebot
import logging
from config import *
from telebot import apihelper
from datetime import datetime
from covid.api import CovId19Data

api = CovId19Data(force=True)

log = logging.getLogger('telebot')
log.setLevel(logging.INFO)
fh = logging.FileHandler("/var/log/tg_telebot.log", 'a', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['test'])
def start(message):
    res = api.get_stats()
    send_text = f'<b>{res}</b>\nВремя проверки - <b>{datetime.now()}</b>\n'
    bot.send_message(message.chat.id, send_text, parse_mode='html')

    # bot.send_message('@covid19word', send_chanel, parse_mode='html')
    log.info(f'Called bot.. name: {message.from_user.first_name}, command: /test')

@bot.message_handler(content_types=['text'])
def mess(message):
    out_message = ''
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'россия':
        location = ''
        # location = covid_19.getLocationByCountryCode('RU')
    else:
        location = ''
        # location = covid_19.getLatest()
        out_message = f'<u>Данные по всему миру:</u>\n<b> Заболевшие: </b>{location["confirmed"]}'
        log.info(f'Called bot.. name: {message.from_user.first_name}, not_command(message):{get_message_bot}')

    if out_message == '':
        date = location[0]['last_updated'].split('T')
        time = date[1].split('.')
        country_population = location[0]["country_population"]
        people_confirmed = location[0]["latest"]["confirmed"]
        percentage_patients_country = (int(people_confirmed) * 100) / int(country_population)
        out_message = f'<b>Страна - {get_message_bot}</b>\n\n' \
                      f'<b>Время запуска проверки - {datetime.now()}</b>\n' \
                      f'<b>Статистика, обновлено (вчера)* в {time[0]} UTC -5</b>\n\n' \
                      f'<b>Население страны - {location[0]["country_population"]:,}</b>\n' \
                      f'<b>Подтверждены всего - {location[0]["latest"]["confirmed"]} *</b>\n' \
                      f'<b>Погибли - {location[0]["latest"]["deaths"]} * </b>\n\n' \
                      f'<b>Процент заболевших в стране - {percentage_patients_country:.7f} % *</b>'

        print(f'Name: {message.from_user.first_name}, Date: {datetime.now()}')
        log.info(f'Called bot.. name: {message.from_user.first_name}, command: {get_message_bot}')


    bot.send_message(message.chat.id, out_message, parse_mode='html')
    # bot.send_message('@covid19word', out_message, parse_mode='html')

while True:
    try:
        bot.polling(none_stop=True)
        break
    except Exception as e:
        log.exception(f'Exception bot.. message: {e}.')
