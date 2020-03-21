# -*- coding: utf-8 -*-
import users_data_controller
import bot_log_controller
import vk_utils
import telebot
import config

from threading import Thread
from telebot import types
from time import sleep

# Инициализация бота
bot = telebot.TeleBot(config.TOKEN)


# При первом запуске бота
@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    # Отправка сообщения "Ну привет, <Имя пользователя>))"
    bot.send_message(message.chat.id,  # В какой чат отправить сообщение
                     # Какое сообщение
                     config.WELCOME_MESSAGE.encode('utf-8').format(message.from_user),
                     # Как форматировать строку
                     parse_mode='html',
                     # Подключаем клавиатуру
                     reply_markup=init_start_keyboard())
    # Инициализация стикера
    sticker = open(config.WELCOME_STICKER, 'rb')
    # Отправка стикера
    bot.send_sticker(message.chat.id, sticker)


# При получении сообщения
@bot.message_handler(content_types=['text'])
def on_message_received(message):
    if message.chat.type == 'private':
        # Получаем идентификатор чата, с которого пришло сообщение
        chat_id = message.chat.id
        msg_text = message.text.encode('utf-8')
        user_id = message.chat.username
        # Если пользователь отправил "Начать" или "Изменить интервал отправки мемов"
        if msg_text == config.START_KEYBOARD_BUTTON or msg_text == config.DEFAULT_KEYBOARD_BUTTON_2:
            bot.send_message(chat_id,  # Идентификатор чата
                             config.START_MESSAGE,  # Сообщение
                             reply_markup=init_intervals_keyboard())  # Клавиатура
        # Если пользователь задал новый интервал отправки мемов
        elif "минут" in msg_text:
            interval = int(msg_text[2:4].encode('utf-8'))
            end_of_every = "ые"
            if interval == 1:
                end_of_every = "ую"
            users_data_controller.add_user_if_needed(user_id, chat_id)
            users_data_controller.change_user_interval(user_id, interval)
            bot.send_message(chat_id,
                             config.INTERVAL_SET_MESSAGE.format(end_of_every, msg_text[2:]),
                             parse_mode='html',
                             reply_markup=init_default_keyboard())
        # Если пользователь запросил новый мем
        elif msg_text == config.DEFAULT_KEYBOARD_BUTTON_1:
            send_mem(chat_id, user_id)


# Возвращает первую клавиатуру
def init_start_keyboard():
    # Инициализация markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Инициализация кнопки
    btn1 = types.KeyboardButton(config.START_KEYBOARD_BUTTON)
    # Добавление кнопки в markup
    markup.add(btn1)
    # Возвращаем markup
    return markup


# Возвращает стандартную клавиатуру
def init_default_keyboard():
    # Инициализация markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Инициализация кнопок
    btn1 = types.KeyboardButton(config.DEFAULT_KEYBOARD_BUTTON_1)
    btn2 = types.KeyboardButton(config.DEFAULT_KEYBOARD_BUTTON_2)
    # Добавление кнопки в markup
    markup.add(btn1)
    markup.add(btn2)
    # Возвращаем markup
    return markup


# Возвращает клавиатуру со списком минут
def init_intervals_keyboard():
    # Инициализация markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавление кнопок в markup
    emojis = ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖']
    # Итератор для эмодзи
    iterator = 0
    for interval in config.INTERVALS:
        minutes_string = "минут"
        if interval == 1:
            minutes_string = "минуту"
        elif interval == 3:
            minutes_string = "минуты"
        # Добавляем новую кнопку в markup
        markup.add(types.KeyboardButton("{0} {1} {2}".format(emojis[iterator], interval, minutes_string)))
        # Увеличиваем итератор
        iterator += 1
    # Возвращаем markup
    return markup


def send_mem(chat_id, user_id):
    url = vk_utils.get_mem(user_id)
    if url != "":
        bot.send_photo(chat_id, url)
        bot_log_controller.log_send_mem(user_id, url)
    else:
        send_mem(chat_id, user_id)


def start_repeat_thread():
    thread = Thread(target=threaded_function)
    thread.start()


def threaded_function():
    print("Start repeat thread.")
    minutes_have_passed_since_the_launch = 0
    while True:
        users_for_distribution = []

        for interval in config.INTERVALS:
            if minutes_have_passed_since_the_launch % interval == 0:
                users = users_data_controller.get_all_users_by_interval(interval)
                users_for_distribution += users

        # Отправить всем пользователям
        counter = 0
        for user in users_for_distribution:
            send_mem(user['chat_id'], user['user_id'])
            counter += 1

        sleep(60)
        minutes_have_passed_since_the_launch += 1
        bot_log_controller.log_elapsed_time(minutes_have_passed_since_the_launch)


# Запуск бота
print("Bot successful started!")
start_repeat_thread()
bot.polling(none_stop=True)
