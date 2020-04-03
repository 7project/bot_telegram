import COVID19Py
import telebot
import logging
from config import *
from telebot import apihelper
from datetime import datetime


log = logging.getLogger('telebot')
log.setLevel(logging.INFO)
fh = logging.FileHandler("telebot.log", 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)


covid_19 = COVID19Py.COVID19()

# PROXY = '154.16.202.22:8080'

# apihelper.proxy = {
#     'http': 'http://' + PROXY,
#     'https': 'https://' + PROXY,
# }

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    send_text = f'<b>Бот статистики COVID-19. Будь начеку, {message.from_user.first_name}!</b>\nВремя проверки - <b>{datetime.now()}</b>\nВведите страну(Россия, США, Украина): '
    bot.send_message(message.chat.id, send_text, parse_mode='html')


@bot.message_handler(content_types=['text'])
def mess(message):
    out_message = ''
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'россия':
        location = covid_19.getLocationByCountryCode('RU')
    elif get_message_bot == 'сша':
        location = covid_19.getLocationByCountryCode('US')
    elif get_message_bot == 'украина':
        location = covid_19.getLocationByCountryCode('UA')
    else:
        location = covid_19.getLatest()
        out_message = f'<u>Данные по всему миру:</u>\n<b> Заболевшие: </b>{location["confirmed"]}'

    if out_message == '':
        date = location[0]['last_updated'].split('T')
        time = date[1].split('.')
        out_message = f'Страна - <b>{get_message_bot}</b>\n' \
                      f'Время проверки - <b>{datetime.now()}</b>\n' \
                      f'Население страны - {location[0]["country_population"]:,} *\n' \
                      f'Потверждены всего - {location[0]["latest"]["confirmed"]:,} *\n' \
                      f'Погибли - {location[0]["latest"]["deaths"]:,} *'

        print(f'Name: {message.from_user.first_name}, Date: {datetime.now()}')
        log.info('Called bot..')


    bot.send_message(message.chat.id, out_message, parse_mode='html')

# счетчик
# count_exp = 0

bot.polling(none_stop=False)

# while True:
#     try:
#         count_exp = 0
#         bot.polling(none_stop=True)
#     except Exception as exp:
#         count_exp += 1
#         print(exp)
#         if count_exp == 3:
#             break

# latest = covid_19.getLatest()
# location = covid_19.getLocationByCountryCode('RU')


# print(latest)
# print()
# print(location)

