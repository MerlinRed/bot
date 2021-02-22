import html
import json

import lxml.html
import pymorphy2
import requests
from bs4 import BeautifulSoup

from load_all import bot
from transliteration import transliteration_data


def take_and_translate_city_for_search(city):
    city_in_english = transliteration_data(data=city)
    return city_in_english


def transform_month(month):
    months_in_numbers = dict(Январь='01', Февраль='02', Март='03', Апрель='04', Май='05', Июнь='06', Июль='07',
                             Август='08', Сентябрь='09',
                             Октябрь='10', Ноябрь='11', Декабрь='12')
    for key, value in months_in_numbers.items():
        if month == key:
            return value


def declension_month(month):
    morph = pymorphy2.MorphAnalyzer()
    declension = morph.parse(f'{month}')[0]
    declension_genitive = declension.inflect({'gent'})
    transliteration_month = transliteration_data(data=declension_genitive.word)
    return transliteration_month


def select_event(message, city, date, concert=False, exhibition=False, performance=False):
    if concert:
        url = f'https://www.culture.ru/afisha/{city}/kontserti?seanceStartDate={date}&seanceEndDate={date}'
        found_events(message=message, url=url)
    elif exhibition:
        url = f'https://www.culture.ru/afisha/{city}/vistavki?seanceStartDate={date}&seanceEndDate={date}'
        found_events(message=message, url=url)
    elif performance:
        url = f'https://www.culture.ru/afisha/{city}/spektakli?seanceStartDate={date}&seanceEndDate={date}'
        found_events(message=message, url=url)


def found_events(message, url):
    try:

        lst_events = []
        response = requests.get(url=url)
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
        sort_events = sorted(set(lst_events), key=lambda x: x[2])
        for event in sort_events:
            bot.send_message(chat_id=message.chat.id,
                             text=f'название - {event[0]}\nадрес - {event[1]}\nначало в - {event[2]}')

    except AttributeError:
        bot.send_message(chat_id=message.chat.id,
                         text='Ничего не найдено.')


def search_cinema(message, city, day_month):
    list_movies = []
    url = f'https://www.afisha.ru/{city}/schedule_cinema/{day_month}/'
    response = requests.get(url=url)
    events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
    for event in events.find_all('section', {'class': 'oIhSV _2nJif like-container'}):
        for genre in event.find_all('a', {'class': 'WR4gB'}):
            pass
        for name in event.find_all('h3', {'class': 'heHLK'}):
            pass
        description = [div for div in event.select('div') if not div.has_attr('class')]
        list_movies.append((genre.get_text(), name.get_text(), description[0].get_text()))

    sort_movies = sorted(set(list_movies))
    for movie in sort_movies:
        bot.send_message(chat_id=message.chat.id,
                         text=f'жанр - {movie[0]}\nназвание - {movie[1]}\nописание - {movie[2]}')
