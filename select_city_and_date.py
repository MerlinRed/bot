from telebot import types

from create_file_with_cities import search_file_with_cites
from load_all import bot


@bot.callback_query_handler(func=lambda callback: True)
def choice_city(callback):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    years = ['2021', '2022', '2023', '2024']
    if callback.data == 'Ввести свой город самостоятельно':
        msg_entered_city = bot.send_message(chat_id=callback.message.chat.id, text='Введите ваш город')
        bot.register_next_step_handler(msg_entered_city, writing_entered_city)

    for char in alphabet:
        if callback.data == char:
            select_name_your_city(callback.message, char)

    for year in years:
        if callback.data == year:
            bot.send_message(chat_id=callback.message.chat.id, text=f'Выбран {callback.data} год')
            months_in_calendar(callback.message)

    if callback.data in ['Январь', 'Март', 'Май', 'Июль', 'Август', 'Октябрь', 'Декабрь']:
        bot.send_message(chat_id=callback.message.chat.id, text=f'Выбран {callback.data} месяц')
        writing_selected_date(callback.data)
        days_in_calendar(callback.message, 31)
    elif callback.data in ['Апрель', 'Июнь', 'Сентябрь', 'Ноябрь']:
        bot.send_message(chat_id=callback.message.chat.id, text=f'Выбран {callback.data} месяц')
        writing_selected_date(callback.data)
        days_in_calendar(callback.message, 30)
    elif callback.data == 'Февраль':
        bot.send_message(chat_id=callback.message.chat.id, text=f'Выбран {callback.data} месяц')
        writing_selected_date(callback.data)
        days_in_calendar(callback.message, 28)

    if callback.data in [str(x) for x in range(1, 31 + 1)]:
        bot.send_message(chat_id=callback.message.chat.id, text=f'Выбран {callback.data} день')
        writing_selected_date(callback.data)


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
    cities = search_file_with_cites(letter)
    inline_button_choice_city = [types.InlineKeyboardButton(text=f'{city}', callback_data=f'{city}') for
                                 city in cities]
    inline_markup_choice_city = types.InlineKeyboardMarkup().add(*inline_button_choice_city)
    bot.send_message(chat_id=message.chat.id, text='Выберите ваш город.',
                     reply_markup=inline_markup_choice_city)
    bot.send_message(chat_id=message.chat.id, text=f'Выбран {message} город')


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
    city = message.text
    bot.send_message(chat_id=message.chat.id, text=f'Вы ввели город - {city}')
    years_in_calendar(message)


def writing_selected_city(message):
    city = message
    bot.send_message(chat_id=message.chat.id, text=f'Вы выбрали город - {city}')
    years_in_calendar(message)


def writing_selected_date(message):
    date = ''
    date += message + '-'
    bot.send_message(chat_id=message.chat.id, text=f'дата {date}')
