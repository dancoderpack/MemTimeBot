# -*- coding: utf-8 -*-
# Token Telegram бота
TOKEN = "1148282016:AAE9WBxSHXzEG30H7w2utMM6JF4ew2ALo6o"

# Token Standalone приложения VK
VK_ACCESS_TOKEN = "9a1ac09b9a1ac09b9a1ac09b769a6aaa6c99a1a9a1ac09bc46fe3207a32ee727b8bdf94"

# Кнопки
START_KEYBOARD_BUTTON = "🔶 НАЧАТЬ 🔶"
DEFAULT_KEYBOARD_BUTTON_1 = "🌇 Получить новый мем!"
DEFAULT_KEYBOARD_BUTTON_2 = "⏰ Изменить интервал отправки мемов"
DEFAULT_KEYBOARD_BUTTON_3 = "🔇 Отключить звук"  # В разработке

# Сообщения
WELCOME_MESSAGE = "Ну привет, <b>{0.first_name}</b>!)))"
START_MESSAGE = "Как часто мне присылать тебе мемы? Через..."
INTERVAL_SET_MESSAGE = "Отлично! Буду присылать тебе мем кажд{0} <b>{1}</b>"

# Идентификаторы пабликов
GROUPS = [-135209264]  # Бот Максим

# Интервалы
INTERVALS = [1, 3, 5, 10, 15, 30, 60]

# Путь до user.json
USERS_JSON_PATH = "/home/dancoder/MemTimeBot/users.json"

# Путь до папки стикеров
PATH_STICKERS = "/home/dancoder/MemTimeBot/stickers/"

# Стикеры
WELCOME_STICKER = PATH_STICKERS + "dancing_bird.tgs"  # Стикер с танцующей птицей
