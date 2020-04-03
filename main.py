import COVID19Py
import telebot
import logging
from config import *
from telebot import apihelper
from datetime import datetime


log = logging.getLogger('telebot')
log.setLevel(logging.INFO)
fh = logging.FileHandler("/var/log/tg_telebot.log", 'w', 'utf-8')
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
    send_text = f'<b>Бот статистики COVID-19. Будь начеку, {message.from_user.first_name}!</b>\nВремя проверки - <b>{datetime.now()}</b>\n' \
                f'Введите страну из списка (США, Испания, Италия, Германия, Китай, Франция, Иран, Англия, Турция, Росиия, Япония, Украина):'
    bot.send_message(message.chat.id, send_text, parse_mode='html')


@bot.message_handler(commands=['map'])
def start(message):
    send_text = f'<b>Карта статистики COVID-19 в мире. Будь начеку, {message.from_user.first_name} - мой руки, сиди дома!</b>\nВремя проверки - <b>{datetime.now()}</b>\n' \
                f'<a href="https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6">Word maps! Press.. me </a>'
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
    elif get_message_bot == 'италия':
        location = covid_19.getLocationByCountryCode('IT')
    elif get_message_bot == 'испания':
        location = covid_19.getLocationByCountryCode('ES')
    elif get_message_bot == 'китай':
        location = covid_19.getLocationByCountryCode('CN')
    elif get_message_bot == 'германия':
        location = covid_19.getLocationByCountryCode('DE')
    elif get_message_bot == 'франция':
        location = covid_19.getLocationByCountryCode('FR')
    elif get_message_bot == 'иран':
        location = covid_19.getLocationByCountryCode('IR')
    elif get_message_bot == 'япония':
        location = covid_19.getLocationByCountryCode('JP')
    elif get_message_bot == 'англия':
        location = covid_19.getLocationByCountryCode('GB')
    elif get_message_bot == 'турция':
        location = covid_19.getLocationByCountryCode('TR')
    else:
        location = covid_19.getLatest()
        out_message = f'<u>Данные по всему миру:</u>\n<b> Заболевшие: </b>{location["confirmed"]}'
        log.info(f'Called bot.. name: {message.from_user.first_name}')

    if out_message == '':
        date = location[0]['last_updated'].split('T')
        time = date[1].split('.')
        country_population = location[0]["country_population"]
        people_confirmed = location[0]["latest"]["confirmed"]
        percentage_patients_country = (int(people_confirmed) * 100) / int(country_population)
        out_message = f'Страна - <b>{get_message_bot}</b>\n' \
                      f'Время запуска проверки - <b>{datetime.now()}</b>\n' \
                      f'Статистика на - <b>{date[0]} - {time[0]}</b>(Фактически за прошлый день!)\n' \
                      f'Население страны - {location[0]["country_population"]:,}\n' \
                      f'Потверждены всего - {location[0]["latest"]["confirmed"]} *\n' \
                      f'Погибли - {location[0]["latest"]["deaths"]} *\n' \
                      f'Процент заболевших в стране - {percentage_patients_country:.7f} % *'

        print(f'Name: {message.from_user.first_name}, Date: {datetime.now()}')
        log.info(f'Called bot.. name: {message.from_user.first_name}, command: {get_message_bot}')


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

