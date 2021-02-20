import html
import json
from load_all import bot
import lxml.html
import requests
from bs4 import BeautifulSoup
from googletrans import Translator


def take_and_translate_city_for_search(city):
    translator = Translator()
    translate_city = translator.translate(city, src='ru', dest='en')
    city_in_english = translate_city.text.lower()
    return city_in_english


def found_concert_events(message, city, date):
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
    bot.send_message(chat_id=message.chat.id, text=lst_events)
