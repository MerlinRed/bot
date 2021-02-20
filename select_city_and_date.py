from afisha import found_exhibition_events
from afisha import take_and_translate_city_for_search, found_concert_events, transform_date, found_performance_events
from handlers import bot
from manipulation_with_cities_file import look_all_cities
from inline_buttons import select_name_your_city, years_in_calendar, months_in_calendar, days_in_calendar
from inline_buttons import difference_events

CITY = None
YEAR = None
MONTH = None
DAY = None
DATE = None


@bot.callback_query_handler(func=lambda callback: True)
def choice_city(callback):
    global YEAR
    global MONTH
    global DAY
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    years = ['2021', '2022', '2023', '2024']
    if callback.data == 'Ввести свой город самостоятельно':
        msg_entered_city = bot.send_message(chat_id=callback.message.chat.id, text='Введите ваш город')
        bot.register_next_step_handler(msg_entered_city, writing_entered_city)

    for char in alphabet:
        if callback.data == char:
            select_name_your_city(message=callback.message, char=char)

    for city in [city for city in look_all_cities()]:
        if callback.data == city:
            writing_selected_city(message=callback.message, city=callback.data)

    for year in years:
        if callback.data == year:
            YEAR = callback.data
            months_in_calendar(message=callback.message)

    if callback.data in ['Январь', 'Март', 'Май', 'Июль', 'Август', 'Октябрь', 'Декабрь']:
        MONTH = callback.data
        days_in_calendar(message=callback.message, quantity_days=31)
    elif callback.data in ['Апрель', 'Июнь', 'Сентябрь', 'Ноябрь']:
        MONTH = callback.data
        days_in_calendar(message=callback.message, quantity_days=30)
    elif callback.data == 'Февраль':
        MONTH = callback.data
        days_in_calendar(message=callback.message, quantity_days=28)

    if callback.data in ['0' + str(x) if x in [1, 2, 3, 4, 5, 6, 7, 8, 9] else str(x) for x in range(1, 31 + 1)]:
        DAY = callback.data
        writing_selected_date(message=callback.message)

    if callback.data == 'Концерты':
        found_concert_events(message=callback.message, city=CITY, date=DATE)

    elif callback.data == 'Спектакли':
        found_performance_events(message=callback.message, city=CITY, date=DATE)

    elif callback.data == 'Выставки':
        found_exhibition_events(message=callback.message, city=CITY, date=DATE)


def writing_entered_city(message):
    global CITY
    CITY = take_and_translate_city_for_search(city=message.text)

    bot.send_message(chat_id=message.chat.id, text=f'Вы ввели город - {CITY}')
    years_in_calendar(message=message)


def writing_selected_city(message, city):
    global CITY
    CITY = take_and_translate_city_for_search(city=city)

    bot.send_message(chat_id=message.chat.id, text=f'Вы выбрали город - {CITY}')
    years_in_calendar(message=message)


def writing_selected_date(message):
    global DATE
    month = transform_date(month=MONTH)
    DATE = YEAR + '-' + month + '-' + DAY
    bot.send_message(chat_id=message.chat.id, text=f'дата - {DATE}')
    difference_events(message)
