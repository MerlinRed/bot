#!/usr/bin/python3
from telebot import types

from authorization import authorization_email, check_user_authorization, exit_user_from_account
from create_file_with_cities import search_file_with_cites
from load_all import bot
from registration import registration, check_registration_user


@bot.message_handler(commands=['start', 'help'])
def start_chat(message):
    keyboard_start_msg = types.ReplyKeyboardMarkup(True, True)
    keyboard_start_msg.row('Авторизоваться', 'Зарегистрироваться', 'Выйти из аккаунта')
    text = 'Для продолжения взаимодействий с ботом необходимо зарегистрироваться и авторизоваться.\n\n' \
           'Если вы уже зарегистрированы, необходимо только авторизоваться.'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard_start_msg)


@bot.message_handler(content_types=['text'])
def auth_reg(message):
    if message.text == 'Авторизоваться':
        if check_user_authorization(user_id=message.from_user.id):
            bot.send_message(chat_id=message.chat.id, text='Вы уже авторизованы.')
            return
        msg_password = bot.send_message(message.chat.id, 'Введите почту для авторизации.\nПример почты: email@mail.ru')
        bot.register_next_step_handler(msg_password, authorization_email)
    elif message.text == 'Зарегистрироваться':
        if check_registration_user(user_id=message.from_user.id):
            bot.send_message(chat_id=message.chat.id, text='Вы уже зарегистрированы.')
            return
        msg = bot.send_message(message.chat.id, 'Введите почту для регистрации.\nПример почты: email@mail.ru')
        bot.register_next_step_handler(msg, registration)
    elif message.text == 'Выйти из аккаунта':
        exit_user_from_account(user_id=message.from_user.id)
        bot.send_message(message.chat.id, 'Вы вышли из аккаунта.')
    elif not check_user_authorization(user_id=message.from_user.id):
        bot.send_message(chat_id=message.chat.id, text='Вы не авторизованы. Доступ к боту закрыт.')
    else:
        # choice_letter_your_city(message)
        calendar(message)


def choice_letter_your_city(message):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    inline_button_enter_your_city = types.InlineKeyboardButton(text='Ввести свой город самостоятельно',
                                                               callback_data='Ввести свой город самостоятельно')
    inline_button_choice_letter = [types.InlineKeyboardButton(text=f'{letter}', callback_data=f'{letter}') for
                                   letter in alphabet]
    inline_markup_choice_letter = types.InlineKeyboardMarkup().add(inline_button_enter_your_city,
                                                                   *inline_button_choice_letter)
    bot.send_message(chat_id=message.chat.id, text='Нажмите на начальную букву вашего города.',
                     reply_markup=inline_markup_choice_letter)


@bot.callback_query_handler(func=lambda callback: True)
def choice_city(callback):
    if callback.data == 'Ввести свой город самостоятельно':
        bot.send_message(chat_id=callback.message.chat.id, text='Введите ваш город')
    else:
        alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
        for char in alphabet:
            if callback.data == char:
                letter = str(char).upper()
                cities = search_file_with_cites(letter)
                inline_button_choice_city = [types.InlineKeyboardButton(text=f'{city}', callback_data=f'{city}') for
                                             city in
                                             cities]
                inline_markup_choice_city = types.InlineKeyboardMarkup().add(*inline_button_choice_city)
                bot.send_message(chat_id=callback.message.chat.id,
                                 text='Выберите ваш город.',
                                 reply_markup=inline_markup_choice_city)


def calendar(message):
    years = [2021, 2022, 2023, 2024]
    inline_button_choice_year = [types.InlineKeyboardButton(text=f'{year}', callback_data=f'{year}') for
                                 year in years]
    inline_markup_choice_year = types.InlineKeyboardMarkup().add(*inline_button_choice_year)
    bot.send_message(chat_id=message.chat.id, text='Выберите интересующий вас год',
                     reply_markup=inline_markup_choice_year)


@bot.callback_query_handler(func=lambda callback: True)
def choice_date_in_calendar(callback):
    years = [2021, 2022, 2023, 2024]
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь', 'Декабрь']
    for year in years:
        if callback.data == year:
            inline_button_choice_month = [types.InlineKeyboardButton(text=f'{month}', callback_data=f'{month}') for
                                          month in months]
            inline_markup_choice_month = types.InlineKeyboardMarkup().add(*inline_button_choice_month)
            bot.send_message(chat_id=callback.message.chat.id, text='Выберите интересующий вас год',
                             reply_markup=inline_markup_choice_month)

        elif callback.data == months:
            inline_button_choice_days = [types.InlineKeyboardButton(text=f'{day}', callback_data=f'{day}') for
                                         day in range(1, 30 + 1)]

            inline_markup_choice_days = types.InlineKeyboardMarkup().add(*inline_button_choice_days)
            bot.send_message(chat_id=callback.message.chat.id, text='Выберите интересующий вас год',
                             reply_markup=inline_markup_choice_days)
