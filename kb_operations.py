from aiogram import  types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_operations import get_race, get_current_position, set_current_position
from random import shuffle


def get_main_kb():
    buttons = [
        [KeyboardButton(text="🎒 путешествия")],
        [KeyboardButton(text="📋 действия"), KeyboardButton(text="🌐 Карта")],
        [KeyboardButton(text="📊 Статистика")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_start_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="🌾 Жнецы", callback_data="btn1"),
        types.InlineKeyboardButton(text="⚔️ Бульдоги", callback_data="btn2"),
        types.InlineKeyboardButton(text="🍃 Листорезы", callback_data="btn3")
    )
    builder.adjust(3)
    return builder.as_markup()

def get_start_confirme_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="🌾 Жнецы", callback_data="btn1"),
        types.InlineKeyboardButton(text="⚔️ Бульдоги", callback_data="btn2"),
        types.InlineKeyboardButton(text="🍃 Листорезы", callback_data="btn3"),
        types.InlineKeyboardButton(text="🔙 Вернуться", callback_data="btn4"),
        types.InlineKeyboardButton(text="✅ подтвердить", callback_data="btn5")
    )
    builder.adjust(3)
    return builder.as_markup()

def get_trips_kb(user_id):
    builder = InlineKeyboardBuilder()
    if get_race(user_id) == "🌾 Жнецы":
        if get_current_position(user_id) == "🏰 колония":
            builder.add(
            types.InlineKeyboardButton(text="🌾 поле", callback_data="travel_field")
            )
            builder.adjust(1)
        if get_current_position(user_id) == "🌾 поле":
            builder.add(
                types.InlineKeyboardButton(text="🏰 колония", callback_data="travel_colony")
            )
            builder.adjust(1)
    return builder.as_markup()

def get_actions_kb(user_id):
    builder = InlineKeyboardBuilder()
    if get_current_position(user_id) == "🏰 колония":
         builder.add(
         types.InlineKeyboardButton(text="просмотреть заказ королевы", callback_data="view_orders")
         )
         builder.adjust(1)
    if get_current_position(user_id) == "🌾 поле":
        builder.add(
            types.InlineKeyboardButton(text="🔎 искать зерно", callback_data="look_for_grain")
        )
        builder.adjust(1)
    return builder.as_markup()

def get_answers_kb(answer, wrong1, wrong2):
    answers = [answer, wrong1, wrong2]
    shuffle(answers)
    right_answer_position = answers.index(answer)
    callback_data_list = ["wrong_answer", "wrong_answer", "wrong_answer"]
    callback_data_list[right_answer_position] = "right_answer"
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text=answers[0], callback_data=callback_data_list[0]),
        types.InlineKeyboardButton(text=answers[1], callback_data=callback_data_list[1]),
        types.InlineKeyboardButton(text=answers[2], callback_data=callback_data_list[2])
    )
    builder.adjust(3)
    return builder.as_markup()
