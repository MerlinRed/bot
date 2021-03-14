import pymorphy2
import requests
from bs4 import BeautifulSoup

from load_all import bot
from transliteration import transliteration_data
from city_db import select_city


def city_name_in_url(city):
    if city == 'москва':
        return 'msk'
    return select_city(rus_city=city)


def declension_month(month):
    morph = pymorphy2.MorphAnalyzer()
    declension = morph.parse(f'{month}')[0]
    declension_genitive = declension.inflect({'gent'})
    transliteration_month = transliteration_data(data=declension_genitive.word)
    return transliteration_month


def select_event(message, city, date, concert=False, exhibition=False, performance=False, movie=False):
    if concert:
        url = f'https://www.afisha.ru/{city}/schedule_concert/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск концертов...')
        search_class = '_3cJdx _2nJif like-container'
        search_concert(message=message, url=url, search_class=search_class)
    elif exhibition:
        url = f'https://www.afisha.ru/{city}/schedule_exhibition/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск выставок...')
        search_exhibition(message=message, url=url)
    elif performance:
        url = f'https://www.afisha.ru/{city}/schedule_theatre/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск спектаклей...')
        search_performance(message=message, url=url)
    elif movie:
        url = f'https://www.afisha.ru/{city}/schedule_cinema/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск фильмов...')
        search_cinema(message=message, url=url)


def search_concert(message, url, search_class):
    try:

        list_concerts = []
        response = requests.get(url=url)
        events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
        for event in events.find_all('section', {'class': search_class}):
            for genre in event.find_all('a', {'class': 'WR4gB'}): ...
            for name in event.find_all('h3', {'class': 'heHLK'}): ...
            for time in event.find_all('div', {'class': '_1Jo7v'}): ...
            description = [div for div in event.select('div') if not div.has_attr('class')]
            description_for_all_events = '' if description == [] else description[0].get_text()
            genre_for_all_events = '' if genre == [] else genre.get_text()
            name_for_all_events = '' if name == [] else name.get_text()
            time_for_all_events = '' if time == [] else time.get_text()
            list_concerts.append(
                (genre_for_all_events, name_for_all_events, time_for_all_events, description_for_all_events))

        sort_concerts = sorted(set(list_concerts), key=lambda x: x[2])
        for concert in sort_concerts:
            bot.send_message(chat_id=message.chat.id, text=f'жанр - {concert[0]}\nназвание - {concert[1]}\n'
                                                           f'место и дата - {concert[2]}\nописание - {concert[3]}')

    except AttributeError:
        bot.send_message(chat_id=message.chat.id, text='Ничего не найдено.')


def search_exhibition(message, url):
    try:
        list_exhibitions = []
        response = requests.get(url=url)
        events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
        for event in events.find_all('section', {'class': '_1ER_u _2nJif like-container'}):
            for genre in event.find_all('a', {'class': 'WR4gB'}): ...
            for name in event.find_all('h3', {'class': 'heHLK'}): ...
            for time in event.find_all('div', {'class': '_1Jo7v'}): ...
            description = [div for div in event.select('div') if not div.has_attr('class')]
            description_for_all_events = '' if description == [] else description[0].get_text()
            genre_for_all_events = '' if genre == [] else genre.get_text()
            name_for_all_events = '' if name == [] else name.get_text()
            time_for_all_events = '' if time == [] else time.get_text()
            list_exhibitions.append(
                (genre_for_all_events, name_for_all_events, time_for_all_events, description_for_all_events))

        sort_exhibitions = sorted(set(list_exhibitions))
        for exhibition in sort_exhibitions:
            bot.send_message(chat_id=message.chat.id, text=f'жанр - {exhibition[0]}\nназвание - {exhibition[1]}\n'
                                                           f'место и дата окончания выстовки - {exhibition[2]}\nописание - {exhibition[3]}')

    except AttributeError:
        bot.send_message(chat_id=message.chat.id, text='Ничего не найдено.')


def search_performance(message, url):
    try:

        list_performance = []
        response = requests.get(url=url)
        events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
        for event in events.find_all('section', {'class': 'jP8J- _2nJif like-container'}):
            for genre in event.find_all('a', {'class': 'WR4gB'}): ...
            for name in event.find_all('h3', {'class': 'heHLK'}): ...
            for time in event.find_all('div', {'class': '_1Jo7v'}): ...
            description = [div for div in event.select('div') if not div.has_attr('class')]
            description_for_all_events = '' if description == [] else description[0].get_text()
            genre_for_all_events = '' if genre == [] else genre.get_text()
            name_for_all_events = '' if name == [] else name.get_text()
            time_for_all_events = '' if time == [] else time.get_text()
            list_performance.append(
                (genre_for_all_events, name_for_all_events, time_for_all_events, description_for_all_events))

        sort_performance = sorted(set(list_performance))
        for performance in sort_performance:
            bot.send_message(chat_id=message.chat.id, text=f'жанр - {performance[0]}\nназвание - {performance[1]}\n'
                                                           f'место и дата - {performance[2]}\nописание - {performance[3]}')
    except AttributeError:
        bot.send_message(chat_id=message.chat.id, text='Ничего не найдено.')


def search_cinema(message, url):
    try:

        list_movies = []
        response = requests.get(url=url)
        events = BeautifulSoup(response.content, 'html.parser').find('div', class_='content content_view_cards')
        for event in events.find_all('section', {'class': 'oIhSV _2nJif like-container'}):
            for genre in event.find_all('a', {'class': 'WR4gB'}): ...
            for name in event.find_all('h3', {'class': 'heHLK'}): ...
            description = [div for div in event.select('div') if not div.has_attr('class')]
            description_for_all_events = '' if description == [] else description[0].get_text()
            genre_for_all_events = '' if genre == [] else genre.get_text()
            name_for_all_events = '' if name == [] else name.get_text()
            list_movies.append((genre_for_all_events, name_for_all_events, description_for_all_events))

        sort_movies = sorted(set(list_movies))
        for movie in sort_movies:
            bot.send_message(chat_id=message.chat.id,
                             text=f'жанр - {movie[0]}\nназвание - {movie[1]}\nописание - {movie[2]}')

    except AttributeError:
        bot.send_message(chat_id=message.chat.id, text='Ничего не найдено.')
