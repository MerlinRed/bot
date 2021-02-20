from afisha import take_and_translate_city_for_search, found_events
from inline_buttons import select_name_your_city, years_in_calendar, months_in_calendar, days_in_calendar
from load_all import bot
from manipulation_with_cities_file import look_all_cities

CITY = None
YEAR = None
MONTH = None
DAY = None


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

    if callback.data in [str(x) for x in range(1, 31 + 1)]:
        DAY = callback.data
        writing_selected_date(message=callback.message)


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
    date = YEAR + '-' + MONTH + '-' + DAY
    found_events(city=CITY, date=date)

    bot.send_message(chat_id=message.chat.id, text=f'дата {date}')
