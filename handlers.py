#!/usr/bin/python3
from telebot import types

from authorization import authorization_email, check_user_authorization, exit_user_from_account
from load_all import bot
from registration import registration, check_registration_user
from select_city_and_date import select_letter_your_city


@bot.message_handler(commands=['start', 'help'])
def start_chat(message):
    keyboard_start_msg = types.ReplyKeyboardMarkup(True, True)
    keyboard_start_msg.row('Авторизоваться', 'Зарегистрироваться', 'Выйти из аккаунта')
    text = 'Бот предоставляет информации о событиях в вашем городе. Чтобы ее получить, напишите слово "афиша".\n\n' \
           'Для продолжения взаимодействий с ботом необходимо зарегистрироваться и авторизоваться.\n\n' \
           'Если вы уже зарегистрированы, необходимо только авторизоваться.'
    bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard_start_msg)


@bot.message_handler(content_types=['text'])
def auth_reg(message):
    if message.text == 'Авторизоваться':
        if check_user_authorization(user_id=message.from_user.id):
            bot.send_message(chat_id=message.from_user.id, text='Вы уже авторизованы.')
            return
        msg_password = bot.send_message(message.from_user.id,
                                        'Введите почту для авторизации.\nПример почты: email@mail.ru')
        bot.register_next_step_handler(msg_password, authorization_email)
    elif message.text == 'Зарегистрироваться':
        if check_registration_user(user_id=message.from_user.id):
            bot.send_message(chat_id=message.from_user.id, text='Вы уже зарегистрированы.')
            return
        msg = bot.send_message(message.from_user.id, 'Введите почту для регистрации.\nПример почты: email@mail.ru')
        bot.register_next_step_handler(msg, registration)
    elif message.text == 'Выйти из аккаунта':
        exit_user_from_account(user_id=message.from_user.id)
        bot.send_message(message.from_user.id, 'Вы вышли из аккаунта.')
    elif not check_user_authorization(user_id=message.from_user.id):
        bot.send_message(chat_id=message.from_user.id, text='Вы не авторизованы. Доступ к боту закрыт.')
    elif message.text.lower() == 'афиша':
        select_letter_your_city(message)
    else:
        bot.send_message(chat_id=message.from_user.id, text='Введите слово "афиша", чтобы продолжить.')
