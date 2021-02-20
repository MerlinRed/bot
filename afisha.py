import html
import json

import lxml.html
import pytils.translit
import requests
from bs4 import BeautifulSoup

from load_all import bot


def take_and_translate_city_for_search(city):
    city_in_english = pytils.translit.translify(city.lower())
    return city_in_english


def transform_date(month):
    months_in_numbers = dict(Январь='01', Февраль='02', Март='03', Апрель='04', Май='05', Июнь='06', Июль='07',
                             Август='08', Сентябрь='09',
                             Октябрь='10', Ноябрь='11', Декабрь='12')
    for key, value in months_in_numbers.items():
        if month == key:
            return value


def found_concert_events(message, city, date):
    try:

        lst_events = []
        response = requests.get(
            f'https://www.culture.ru/afisha/{city}/kontserti?seanceStartDate={date}&seanceEndDate={date}')
        events = BeautifulSoup(response.content, 'html.parser').find('div',
                                                                     class_='entity-cards grid-1-noSpaceTop_notebook-4_tablet-medium-3_mobile-large-2')
        for event in events.find_all('script'):
            data = lxml.html.fromstring(str(event))
            js = json.loads(html.unescape(data.xpath('//script[@type="application/ld+json"]/text()')[0]))
            name_event = js['name']
            # print(js['location']['name'])
            location_event = js['location']['address']
            for time in events.find_all('div', {'class': 'tile-date_time'}):
                lst_events.append((name_event, location_event, time.get_text()))
        lst_events.sort(key=lambda x: x[2])
        for event in lst_events:
            bot.send_message(chat_id=message.chat.id,
                             text=f'название - {event[0]}\nадрес - {event[1]}\nначало в - {event[2]}')

    except AttributeError:
        bot.send_message(chat_id=message.chat.id, text='Ничего не найдено.')
