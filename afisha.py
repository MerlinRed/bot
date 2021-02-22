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


def select_event(message, city, date, concert=False, exhibition=False, performance=False, movie=False):
    if concert:
        url = f'https://www.afisha.ru/{city}/schedule_concert/{date}/'
        search_concert(message=message, url=url)
    elif exhibition:
        url = f'https://www.afisha.ru/{city}/schedule_exhibition/{date}/'
        search_exhibition(message=message, url=url)
    elif performance:
        url = f'https://www.afisha.ru/{city}/schedule_theatre/{date}/'
        search_performance(message=message, url=url)
    elif movie:
        url = f'https://www.afisha.ru/{city}/schedule_cinema/{date}/'
        search_cinema(message=message, url=url)


def search_concert(message, url):
    list_concerts = []
    response = requests.get(url=url)
    events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
    for event in events.find_all('section', {'class': '_3cJdx _2nJif like-container'}):
        for genre in event.find_all('a', {'class': 'WR4gB'}): ...
        for name in event.find_all('h3', {'class': 'heHLK'}): ...
        for time in event.find_all('div', {'class': '_1Jo7v'}): ...
        description = [div for div in event.select('div') if not div.has_attr('class')]
        sort_concerts = sorted(set(list_concerts))
        try:
            list_concerts.append((genre.get_text(), name.get_text(), time.get_text(), description[0].get_text()))
            for concert in sort_concerts:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {concert[0]}\nназвание - {concert[1]}\n' \
                                      f'место и дата - {concert[2]}\nописание - {concert[3]}')
        except IndexError:
            list_concerts.append((genre.get_text(), name.get_text()))
            for concert in sort_concerts:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {concert[0]}\nназвание - {concert[1]}\nместо и дата - {concert[2]}')


def search_exhibition(message, url):
    list_exhibitions = []
    response = requests.get(url=url)
    events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
    for event in events.find_all('section', {'class': '_1ER_u _2nJif like-container'}):
        for genre in event.find_all('a', {'class': 'WR4gB'}): ...
        for name in event.find_all('h3', {'class': 'heHLK'}): ...
        for time in event.find_all('div', {'class': '_1Jo7v'}): ...
        description = [div for div in event.select('div') if not div.has_attr('class')]
        sort_exhibitions = sorted(set(list_exhibitions))
        try:
            list_exhibitions.append((genre.get_text(), name.get_text(), time.get_text(), description[0].get_text()))
            for exhibition in sort_exhibitions:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {exhibition[0]}\nназвание - {exhibition[1]}\n' \
                                      f'место и дата окончания выстовки - {exhibition[2]}\nописание - {exhibition[3]}')
        except IndexError:
            list_exhibitions.append((genre.get_text(), name.get_text()))
            for exhibition in sort_exhibitions:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {exhibition[0]}\nназвание - {exhibition[1]}\n' \
                                      f'место и дата окончания выстовки - {exhibition[2]}')


def search_performance(message, url):
    list_performance = []
    response = requests.get(url=url)
    events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
    for event in events.find_all('section', {'class': 'jP8J- _2nJif like-container'}):
        for genre in event.find_all('a', {'class': 'WR4gB'}): ...
        for name in event.find_all('h3', {'class': 'heHLK'}): ...
        for time in event.find_all('div', {'class': '_1Jo7v'}): ...
        description = [div for div in event.select('div') if not div.has_attr('class')]
        sort_performance = sorted(set(list_performance))
        try:
            list_performance.append((genre.get_text(), name.get_text(), time.get_text(), description[0].get_text()))
            for performance in sort_performance:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {performance[0]}\nназвание - {performance[1]}\n' \
                                      f'место и дата - {performance[2]}\nописание - {performance[3]}')
        except IndexError:
            list_performance.append((genre.get_text(), name.get_text()))
            for performance in sort_performance:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {performance[0]}\nназвание - {performance[1]}\n' \
                                      f'место и дата - {performance[2]}')


def search_cinema(message, url):
    list_movies = []
    response = requests.get(url=url)
    events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
    for event in events.find_all('section', {'class': 'oIhSV _2nJif like-container'}):
        for genre in event.find_all('a', {'class': 'WR4gB'}): ...
        for name in event.find_all('h3', {'class': 'heHLK'}): ...
        description = [div for div in event.select('div') if not div.has_attr('class')]
        sort_movies = sorted(set(list_movies))
        try:
            list_movies.append((genre.get_text(), name.get_text(), description[0].get_text()))
            for movie in sort_movies:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {movie[0]}\nназвание - {movie[1]}\nописание - {movie[2]}')
        except IndexError:
            list_movies.append((genre.get_text(), name.get_text()))
            for movie in sort_movies:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {movie[0]}\nназвание - {movie[1]}')
