from dataclasses import dataclass

from telebot import types

from afisha import city_name_in_url, select_event, declension_month
from load_all import bot
from manipulation_with_cities_file import look_all_cities
from manipulation_with_cities_file import search_file_with_cites


@dataclass
class City:
    city: str


@dataclass
class Date:
    month: str
    day: str


@bot.callback_query_handler(func=lambda callback: True)
def choice_city(callback):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЧШЩЭЮЯ'
    if callback.data == 'Ввести свой город самостоятельно':
        msg_entered_city = bot.send_message(chat_id=callback.message.from_user.id, text='Введите ваш город')
        bot.register_next_step_handler(msg_entered_city, writing_entered_city)

    for char in alphabet:
        if callback.data == char:
            select_name_your_city(message=callback.message, char=char)

    for city in [city for city in look_all_cities()]:
        if callback.data == city:
            writing_selected_city(message=callback.message, city=callback.data)

    if callback.data in ['Январь', 'Март', 'Май', 'Июль', 'Август', 'Октябрь', 'Декабрь']:
        Date.month = declension_month(month=callback.data)
        days_in_calendar(message=callback.message, quantity_days=31)
    elif callback.data in ['Апрель', 'Июнь', 'Сентябрь', 'Ноябрь']:
        Date.month = declension_month(month=callback.data)
        days_in_calendar(message=callback.message, quantity_days=30)
    elif callback.data == 'Февраль':
        Date.month = declension_month(month=callback.data)
        days_in_calendar(message=callback.message, quantity_days=28)

    if callback.data in ['0' + str(x) if x in [1, 2, 3, 4, 5, 6, 7, 8, 9] else str(x) for x in range(1, 31 + 1)]:
        Date.day = callback.data
        difference_events(callback.message)

    if callback.data == 'Концерты':
        select_event(message=callback.message, city=City.city, date=f'{Date.day}-{Date.month}', concert=True)

    elif callback.data == 'Театр':
        select_event(message=callback.message, city=City.city, date=f'{Date.day}-{Date.month}', performance=True)

    elif callback.data == 'Выставки':
        select_event(message=callback.message, city=City.city, date=f'{Date.day}-{Date.month}', exhibition=True)

    elif callback.data == 'Кино':
        select_event(message=callback.message, city=City.city, date=f'{Date.day}-{Date.month}', movie=True)


def select_letter_your_city(message):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЧШЩЭЮЯ'
    inline_button_enter_your_city = types.InlineKeyboardButton(text='Ввести свой город самостоятельно',
                                                               callback_data='Ввести свой город самостоятельно')
    inline_button_choice_letter = [types.InlineKeyboardButton(text=f'{letter}', callback_data=f'{letter}') for
                                   letter in alphabet]
    inline_markup_choice_letter = types.InlineKeyboardMarkup().add(inline_button_enter_your_city,
                                                                   *inline_button_choice_letter)
    bot.send_message(chat_id=message.from_user.id,
                     text='Нажмите на начальную букву вашего города.' \
                          '\nЕсли вашего города нет в списке, введите его самостоятельно.',
                     reply_markup=inline_markup_choice_letter)


def select_name_your_city(message, char):
    letter = str(char).upper()
    cities = search_file_with_cites(letter=letter)
    inline_button_choice_city = [types.InlineKeyboardButton(text=f'{city}', callback_data=f'{city}') for
                                 city in cities]
    inline_markup_choice_city = types.InlineKeyboardMarkup().add(*inline_button_choice_city)
    bot.send_message(chat_id=message.from_user.id, text='Выберите ваш город.',
                     reply_markup=inline_markup_choice_city)


def months_in_calendar(message):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь', 'Декабрь']
    inline_button_choice_month = [types.InlineKeyboardButton(text=f'{month}', callback_data=f'{month}') for
                                  month in months]
    inline_markup_choice_month = types.InlineKeyboardMarkup().add(*inline_button_choice_month)
    bot.send_message(chat_id=message.from_user.id, text='Выберите интересующий вас месяц',
                     reply_markup=inline_markup_choice_month)


def days_in_calendar(message, quantity_days):
    days = ['0' + str(x) if x in [1, 2, 3, 4, 5, 6, 7, 8, 9] else str(x) for x in range(1, quantity_days + 1)]
    inline_button_choice_day = [types.InlineKeyboardButton(text=f'{day}', callback_data=f'{day}') for
                                day in days]
    inline_markup_choice_day = types.InlineKeyboardMarkup().add(*inline_button_choice_day)
    bot.send_message(chat_id=message.from_user.id, text='Выберите интересующий вас день',
                     reply_markup=inline_markup_choice_day)


def difference_events(message):
    inline_button_concert = types.InlineKeyboardButton(text='Концерты', callback_data='Концерты')
    inline_button_cinema = types.InlineKeyboardButton(text='Кино', callback_data='Кино')
    inline_button_performance = types.InlineKeyboardButton(text='Театр', callback_data='Театр')
    inline_button_exhibition = types.InlineKeyboardButton(text='Выставки', callback_data='Выставки')
    inline_markup_choice_event = types.InlineKeyboardMarkup().add(inline_button_concert, inline_button_cinema,
                                                                  inline_button_performance,
                                                                  inline_button_exhibition)
    bot.send_message(chat_id=message.from_user.id, text='Выберите интересующее вас мероприятие',
                     reply_markup=inline_markup_choice_event)


def writing_entered_city(message):
    City.city = city_name_in_url(city=message.text.lower())
    months_in_calendar(message=message)


def writing_selected_city(message, city):
    City.city = city_name_in_url(city=city.lower())
    months_in_calendar(message=message)
