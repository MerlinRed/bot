from telebot import types

from afisha import take_and_translate_city_for_search, found_concert_events
from load_all import bot
from manipulation_with_cities_file import look_all_cities
from manipulation_with_cities_file import search_file_with_cites

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


def select_letter_your_city(message):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    inline_button_enter_your_city = types.InlineKeyboardButton(text='Ввести свой город самостоятельно',
                                                               callback_data='Ввести свой город самостоятельно')
    inline_button_choice_letter = [types.InlineKeyboardButton(text=f'{letter}', callback_data=f'{letter}') for
                                   letter in alphabet]
    inline_markup_choice_letter = types.InlineKeyboardMarkup().add(inline_button_enter_your_city,
                                                                   *inline_button_choice_letter)
    bot.send_message(chat_id=message.chat.id, text='Нажмите на начальную букву вашего города.',
                     reply_markup=inline_markup_choice_letter)


def select_name_your_city(message, char):
    letter = str(char).upper()
    cities = search_file_with_cites(letter=letter)
    inline_button_choice_city = [types.InlineKeyboardButton(text=f'{city}', callback_data=f'{city}') for
                                 city in cities]
    inline_markup_choice_city = types.InlineKeyboardMarkup().add(*inline_button_choice_city)
    bot.send_message(chat_id=message.chat.id, text='Выберите ваш город.',
                     reply_markup=inline_markup_choice_city)


def years_in_calendar(message):
    years = ['2021', '2022', '2023', '2024']
    inline_button_choice_year = [types.InlineKeyboardButton(text=f'{year}', callback_data=f'{year}') for
                                 year in years]
    inline_markup_choice_year = types.InlineKeyboardMarkup().add(*inline_button_choice_year)
    bot.send_message(chat_id=message.chat.id, text='Выберите интересующий вас год',
                     reply_markup=inline_markup_choice_year)


def months_in_calendar(message):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь', 'Декабрь']
    inline_button_choice_month = [types.InlineKeyboardButton(text=f'{month}', callback_data=f'{month}') for
                                  month in months]
    inline_markup_choice_month = types.InlineKeyboardMarkup().add(*inline_button_choice_month)
    bot.send_message(chat_id=message.chat.id, text='Выберите интересующий вас месяц',
                     reply_markup=inline_markup_choice_month)


def days_in_calendar(message, quantity_days):
    days = [str(x) for x in range(1, quantity_days + 1)]
    inline_button_choice_day = [types.InlineKeyboardButton(text=f'{day}', callback_data=f'{day}') for
                                day in days]
    inline_markup_choice_day = types.InlineKeyboardMarkup().add(*inline_button_choice_day)
    bot.send_message(chat_id=message.chat.id, text='Выберите интересующий вас день',
                     reply_markup=inline_markup_choice_day)


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
    bot.send_message(chat_id=message.chat.id, text=f'дата - {date}')
    found_concert_events(message=message, city=CITY, date=date)

    bot.send_message(chat_id=message.chat.id, text=f'дата {date}')
