from aiogram import types

kb = [
        [
            types.KeyboardButton(text="Добавить Событие"),
            types.KeyboardButton(text="Список Событий"),
        ],
    ]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb)