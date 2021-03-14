import requests
from bs4 import BeautifulSoup

from city_db import select_city
from load_all import bot


def city_name_in_url(city):
    if city == 'москва':
        return 'msk'
    return select_city(rus_city=city)


def declension_month(month):
    months = {'Январь': 'yanvarya', 'Февраль': 'fevralya', 'Март': 'marta', 'Апрель': 'aprelya',
              'Май': 'maya', 'Июнь': 'iunya', 'Июль': 'iulya', 'Август': 'avgusta', 'Сентябрь': 'sentyabrya',
              'Октябрь': 'oktyabrya', 'Ноябрь': 'noyabrya', 'Декабрь': 'dekabrya'
              }
    return months[month]


def select_event(message, city, date, concert=False, exhibition=False, performance=False, movie=False):
    if concert:
        url = f'https://www.afisha.ru/{city}/schedule_concert/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск концертов...')
        search_class = '_3cJdx _2nJif like-container'
        search_events(message=message, url=url, search_class=search_class)
    elif exhibition:
        url = f'https://www.afisha.ru/{city}/schedule_exhibition/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск выставок...')
        search_class = '_1ER_u _2nJif like-container'
        search_events(message=message, url=url, search_class=search_class)
    elif performance:
        url = f'https://www.afisha.ru/{city}/schedule_theatre/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск спектаклей...')
        search_class = 'jP8J- _2nJif like-container'
        search_events(message=message, url=url, search_class=search_class)
    elif movie:
        url = f'https://www.afisha.ru/{city}/schedule_cinema/{date}/'
        bot.send_message(chat_id=message.chat.id, text='Идет поиск фильмов...')
        search_class = 'oIhSV _2nJif like-container'
        search_events(message=message, url=url, search_class=search_class)


def search_events(message, url, search_class):
    try:

        list_events = []
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
            if search_class != 'oIhSV _2nJif like-container':
                time_for_all_events = '' if time == [] else time.get_text()
                list_events.append(
                    (genre_for_all_events, name_for_all_events, time_for_all_events, description_for_all_events))
            else:
                list_events.append(
                    (genre_for_all_events, name_for_all_events, description_for_all_events))

        if search_class == 'oIhSV _2nJif like-container':
            sort_events = sorted(set(list_events), key=lambda x: x[0])
            for events in sort_events:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'жанр - {events[0]}\nназвание - {events[1]}\nописание - {events[2]}')
        else:
            sort_events = sorted(set(list_events), key=lambda x: x[2][-6:-1])
            for events in sort_events:
                bot.send_message(chat_id=message.chat.id, text=f'жанр - {events[0]}\nназвание - {events[1]}\n'
                                                               f'место и дата - {events[2]}\nописание - {events[3]}')

    except AttributeError:
        bot.send_message(chat_id=message.chat.id, text='Ничего не найдено.')
