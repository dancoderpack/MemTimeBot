# -*- coding: cp1251 -*-
import json
import bot_log_controller
import config


# Возвращает всех наших пользователей, которые хранятся в файле <users.json>
def get_users():
    return json.load(open(config.USERS_JSON_PATH, 'r'))


# Обновляет файл <users.json> изменяя конфигурацию пользователя
def update_user(user_id, interval=-1, counter=-1, chat_id=""):
    users = get_users()
    user = {}
    if counter != 0 or interval != 0:
        user = users[user_id]
    if counter != -1:
        user['counter'] = counter
    if interval != -1:
        user['interval'] = interval
    if chat_id != "":
        user['chat_id'] = chat_id
    users[user_id] = user
    open(config.USERS_JSON_PATH, 'w').write(json.dumps(users))


# Изменяет интервал отправки мемов для конкретного пользователя
def change_user_interval(user_id, interval):
    update_user(user_id, interval)
    bot_log_controller.log_change_user_interval(user_id, interval)


# Изменяет счетчик мемов для конкретного пользователя
def change_user_counter(user_id):
    update_user(user_id, counter=get_counter_value(user_id) + 1)


# Добавляет нового пользователя в файл <users.json>
def add_user_if_needed(user_id, chat_id):
    if user_id not in get_users():
        update_user(user_id, 0, 0, chat_id)
        bot_log_controller.log_add_user_to_db(user_id)


def get_counter_value(user_id):
    return get_users()[user_id]['counter']


def get_interval_value(user_id):
    return get_users()[user_id]['interval']


def get_all_users_by_interval(interval):
    users = get_users()
    result = []
    for user_id in users.keys():
        if users[user_id]['interval'] == interval:
            user = users[user_id]
            user['user_id'] = user_id
            result.append(user)
    return result
