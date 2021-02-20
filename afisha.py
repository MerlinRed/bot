import datetime
import html
import json

import lxml.html
import requests
from bs4 import BeautifulSoup
from googletrans import Translator


def take_and_translate_city_for_search(city):
    translator = Translator()
    translate_city = translator.translate(city, src='ru', dest='en')
    city_in_english = translate_city.text.lower()
    return city_in_english


def time_transformation(time):
    unformat_time = time.split('+')
    moscow_time = unformat_time[0]
    plus_region_time = unformat_time[1]
    type_time_moscow = datetime.datetime.strptime(moscow_time, '%H:%M:%S').time()
    type_time_region = datetime.datetime.strptime(plus_region_time, '%H:%M').time()
    delta_moscow = datetime.timedelta(hours=type_time_moscow.hour, minutes=type_time_moscow.minute)
    delta_region = datetime.timedelta(hours=type_time_region.hour, minutes=type_time_region.minute)
    format_time = delta_moscow + delta_region
    return format_time


def found_events(city, date):
    lst_events = []
    response = requests.get(
        f'https://www.culture.ru/afisha/{city}/kontserti?seanceStartDate={date}&seanceEndDate={date}')
    name = BeautifulSoup(response.content, 'html.parser').find('div',
                                                               class_='entity-cards grid-1-noSpaceTop_notebook-4_tablet-medium-3_mobile-large-2')
    for loc in name.find_all('script'):
        data = lxml.html.fromstring(str(loc))
        js = json.loads(html.unescape(data.xpath('//script[@type="application/ld+json"]/text()')[0]))
        name_event = js['name']
        # print(js['location']['name'])
        location_event = js['location']['address']
        start_date = str(time_transformation(js['startDate'][11:]))
        lst_events.append((name_event, location_event, start_date))
    return lst_events


