import logging
import random

from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from aiogram.enums import ChatType
from users_db_operations import (
    init_db,
    add_user,
    set_race, get_race,
    set_is_race_selected, get_is_race_selected,
    set_current_action, get_current_action,
    set_current_position, get_current_position,
    set_question_id, get_question_id,
    set_grain_storage, get_grain_storage,
    set_all_collecting_bonus, get_all_collecting_bonus
)
from text_operations import load_text
from kb_operations import (
    get_main_kb,
    get_start_kb,
    get_start_confirme_kb,
    get_trips_kb, get_actions_kb,
    get_answers_kb
)
from questions_db_operations import init_questions_db, get_random_question_by_subject, get_explanation_and_answer_by_id
from dotenv import load_dotenv
import os


# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv(".env")
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Токен бота не найден. Проверьте файл .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.chat.type != ChatType.PRIVATE:
        await message.answer("⚠️ Этот бот работает только в личных сообщениях. Пожалуйста, напишите мне в личку.")
        return
    user_id = message.from_user.id
    add_user(user_id)
    if get_is_race_selected(user_id) == "❌ нет":

        global welcome_text
        welcome_text = load_text("welcome_text.txt")

        try:
            photo = FSInputFile("pictures/map.png")
            await message.answer_photo(
                photo=photo,
                caption=welcome_text,
                reply_markup=get_start_kb(),
                parse_mode="HTML"
            )
        except FileNotFoundError:
            logger.error("❌ Файл с картой не найден")
            await message.answer(
                text=welcome_text,
                reply_markup=get_start_kb(),
                parse_mode="HTML"
            )
    else:
        photo_race = {
            "🌾 Жнецы": "pictures/reaper_photo.jpeg",
            "⚔️ Бульдоги": "pictures/bulldog_photo.jpeg",
            "🍃 листорезы": "pictures/leaf_cutter_photo.jpeg"
        }
        action = get_current_action(user_id)
        current_grain, max_grain, grain_str = get_grain_storage(user_id)
        if action == "0": action = "нет"
        caption = f'''
        👋 Привет!\n
🐜 Раса: {get_race(user_id)}
🗺 Текущее положение: {get_current_position(user_id)}
📋 Активное действие: {action}
📦 Текущие запасы:
          🌾 Зерно: {grain_str}
        '''
        try:
            # Отправляем новое сообщение с фото и новыми кнопками
            photo_path = photo_race[get_race(user_id)]
            photo = FSInputFile(photo_path)
            await message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=get_main_kb(),
                parse_mode="HTML"
            )

        except FileNotFoundError:
            logger.error(f"Файл {photo_path} не найден")
            # Если фото не найдено, отправляем просто текст
            await message.answer(
                text=caption,
                reply_markup=get_main_kb(),
                parse_mode="HTML"
            )
        if get_question_id(user_id) != 0:
            question_id, subject, question, explanation, answer, wrong1, wrong2 = get_explanation_and_answer_by_id(get_question_id(user_id))
            if get_current_action(user_id) == "🌾 поиск зерна":
                text = f"🌾 Ответь на вопрос, чтобы найти зерно:\n\n{question}"
            await message.answer(
                text=text,
                reply_markup=get_answers_kb(answer, wrong1, wrong2),
                parse_mode="HTML"
            )

@dp.callback_query(F.data.startswith("btn"))
async def race_choice(callback: types.CallbackQuery):
    btn_number = callback.data[-1]
    user_id = callback.from_user.id
    r = None
    if get_is_race_selected(user_id) == "❌ нет":
        # Определяем текст в зависимости от кнопки
        if btn_number == "1":
          text = load_text("reaper_text.txt")
          set_race(user_id,"🌾 Жнецы")
        elif btn_number == "2":
          text = load_text("bulldog_text.txt")
          set_race(user_id, "⚔️ Бульдоги")
        elif btn_number == "3":
          text = load_text("leaf_cutter_text.txt")
          set_race(user_id, "🍃 листорезы")
        elif btn_number == "4":
          text = welcome_text
        else:
            text = "❓ Неизвестная команда"

        photo_race = {
          "🌾 Жнецы": "pictures/reaper_photo.jpeg",
          "⚔️ Бульдоги": "pictures/bulldog_photo.jpeg",
          "🍃 листорезы": "pictures/leaf_cutter_photo.jpeg"
        }
        try:
         if btn_number in ["1", "2", "3"]:

            # Для кнопок выбора расы - меняем фото
            photo_path = photo_race[get_race(user_id)]
            photo = FSInputFile(photo_path)

            # Создаем медиа объект с новым фото
            media = types.InputMediaPhoto(
                media=photo,
                caption=text,
                parse_mode="HTML"
            )

            # Редактируем сообщение с новым фото
            await callback.message.edit_media(
                media=media,
                reply_markup=get_start_confirme_kb()
            )

         elif btn_number == "4":
            # Для кнопки "Назад" - возвращаем карту
            photo = FSInputFile("pictures/map.png")
            media = types.InputMediaPhoto(
                media=photo,
                caption=text,
                parse_mode="HTML"
            )
            await callback.message.edit_media(
                media=media,
                reply_markup=get_start_kb()
            )
        except FileNotFoundError:
            logger.error(f"❌ Файл не найден: {photo_path}")
            # Если фото не найдено, просто редактируем текст
            await callback.message.edit_caption(
               caption=text,
               reply_markup=get_start_kb(),
              parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")
        if btn_number == "5" and get_race(user_id) != "0":

            set_is_race_selected(user_id,"✅ да")

            race_c = {"🌾 Жнецы": "Зерноградскую Империю🌾",
                      "⚔️ Бульдоги": "Клан Кровавого Жала⚔️",
                      "🍃 листорезы": "Грибную Гегемонию Атлан🍃"}
            r = race_c[get_race(user_id)]
            if r == "Зерноградскую Империю🌾": set_all_collecting_bonus(1)
            try:
                # Отправляем новое сообщение с фото и новыми кнопками
                photo_path = photo_race[get_race(user_id)]
                photo = FSInputFile(photo_path)

                await callback.message.answer_photo(
                    photo=photo,
                    caption=f"🎉 Поздравляем! Вы выбрали {r}\n\nТеперь вы можете управлять своей колонией",
                    reply_markup=get_main_kb(),
                    parse_mode="HTML"
                )

                # Удаляем старое сообщение с выбором рас
                await callback.message.delete()

            except FileNotFoundError:
                logger.error(f"Файл {photo_path} не найден")
                # Если фото не найдено, отправляем просто текст
                await callback.message.answer(
                    text=f"🎉 Поздравляем! Вы выбрали {r}\n\nТеперь вы можете управлять своей колонией",
                    reply_markup=get_main_kb(),
                    parse_mode="HTML"
                )
                await callback.message.delete()

    else:
            await callback.message.delete()
            await callback.answer("⚠ Вы уже выбрали рассу", show_alert=False)


    await callback.answer()


@dp.message(F.text.in_(["🎒 путешествия", "🌐 Карта", "📋 действия", "📊 Статистика"]))
async def handle_menu_buttons(message: types.Message):
    user_id = message.from_user.id
    if get_is_race_selected(user_id) == "❌ нет" or get_is_race_selected(user_id) == None or get_current_action(user_id) != "0":
        return 0
    if message.text == "🎒 путешествия":
            await message.answer(
               text=f"🎒 Выберите куда вы хотите отправиться",
               reply_markup=get_trips_kb(user_id),
               parse_mode="HTML"
            )

    elif message.text == "🌐 Карта":
            try:
                photo = FSInputFile("pictures/map.png")
                await message.answer_photo(
                    photo=photo,
                    caption="🌐 Карта мира Antoria",
                    parse_mode="HTML"
                )
            except Exception as e:
               await message.answer("❌ Не удалось загрузить карту")
               print(f"Ошибка загрузки карты: {e}")

    if message.text == "📋 действия":
        await message.answer(
            text="доступные действия:",
            reply_markup=get_actions_kb(user_id),
            parse_mode="HTML"
        )

    elif message.text == "📊 Статистика":
        photo_race = {
            "🌾 Жнецы": "pictures/reaper_photo.jpeg",
            "⚔️ Бульдоги": "pictures/bulldog_photo.jpeg",
            "🍃 листорезы": "pictures/leaf_cutter_photo.jpeg"
        }
        action = get_current_action(user_id)
        current_grain, max_grain, grain_str = get_grain_storage(user_id)
        if action == "0": action = "нет"
        caption = f'''
🐜 Раса: {get_race(user_id)}
🗺 Текущее положение: {get_current_position(user_id)}
📋 Активное действие: {action}
📦 Текущие запасы:
          🌾 Зерно: {grain_str}
       '''
        try:
            # Отправляем новое сообщение с фото и новыми кнопками
            photo_path = photo_race[get_race(user_id)]
            photo = FSInputFile(photo_path)
            await message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=get_main_kb(),
                parse_mode="HTML"
            )

        except FileNotFoundError:
            logger.error(f"Файл {photo_path} не найден")
            # Если фото не найдено, отправляем просто текст
            await message.answer(
                text=caption,
                reply_markup=get_main_kb(),
                parse_mode="HTML"
            )

@dp.callback_query(F.data.startswith("travel_"))
async def handle_travel_choice(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    travel_location = callback.data.split("_")[1]

    # Устанавливаем новую позицию
    if travel_location == "field":
        set_current_position(user_id, "🌾 поле")
        new_caption = "Ты пришел в поле"
        photo_path = "pictures/field_photo.jpg"
    elif travel_location == "colony":
        set_current_position(user_id, "🏰 колония")
        new_caption = "Ты вернулся в колонию"
        photo_race = {
            "🌾 Жнецы": "pictures/reaper_photo.jpeg",
            "⚔️ Бульдоги": "pictures/bulldog_photo.jpeg",
            "🍃 листорезы": "pictures/leaf_cutter_photo.jpeg"
        }
        photo_path = photo_race[get_race(user_id)]
    else:
        await callback.answer("❌ Неизвестная локация")
        return

    try:
        photo = FSInputFile(photo_path)
        media = types.InputMediaPhoto(
            media=photo,
            caption=new_caption,
            parse_mode="HTML"
        )

        # Редактируем сообщение (фото + текст + клавиатура)
        await callback.message.edit_media(
            media=media,
        )
    except FileNotFoundError:
        logger.error(f"❌ Файл не найден: {photo_path}")
        # Если фото не найдено, меняем только текст и клавиатуру
        await callback.message.edit_caption(
            caption=new_caption,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"❌ Ошибка при редактировании сообщения: {e}")
        await callback.answer("⚠️ Произошла ошибка", show_alert=True)
    finally:
        await callback.answer()

@dp.callback_query(F.data.startswith("look_for_"))
async def handle_looking_for(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if get_question_id(user_id) != 0:
        return 0
    looking_for = callback.data.split("_")[2]
    if looking_for == "grain" and get_current_position(user_id) == "🌾 поле":
        set_current_action(user_id, "🌾 поиск зерна")
        question_id, subject, question, explanation, answer, wrong1, wrong2 = get_random_question_by_subject("📐 математика")
        set_question_id(user_id, question_id)
        await callback.message.edit_text(
            text=f"🌾 Ответь на вопрос, чтобы найти зерно:\n\n{question}",
            reply_markup=get_answers_kb(answer, wrong1, wrong2),
            parse_mode="HTML"
        )


@dp.callback_query(F.data.startswith("answer_"))
async def handle_questions(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Проверяем, есть ли активный вопрос у пользователя
    if get_question_id(user_id) == 0:
        await callback.answer("Нет активного вопроса")
        return

    which_answer = callback.data.split("_")[1]
    question_data = get_explanation_and_answer_by_id(get_question_id(user_id))

    if not question_data:
        await callback.answer("Ошибка: вопрос не найден")
        return

    question_id, subject, question, explanation, answer, wrong1, wrong2 = question_data

    # Сбрасываем ID текущего вопроса
    set_question_id(user_id, 0)

    if which_answer == "right":
        await callback.message.edit_text(
            text=f"✅ Верно!\n\n💡 Пояснение:\n{explanation}",
            parse_mode="HTML"
        )
        print(f"Пользователь {user_id} ✅ верно ответил на вопрос: {question_id}")

        # Получаем текущее действие пользователя
        current_action = get_current_action(user_id)

        # Проверяем, соответствует ли действие поиску зерна
        if current_action == "🌾 поиск зерна":
            bonus = get_all_collecting_bonus(user_id)
            current_grain, max_grain, grain_str = get_grain_storage(user_id)
            amount = random.randint(1, 5) + bonus
            if amount + current_grain > max_grain: set_grain_storage(user_id, max_grain)
            else: set_grain_storage(user_id, amount + current_grain)
            current_grain, max_grain, grain_str = get_grain_storage(user_id)
            try:
                photo = FSInputFile("pictures/grain.jpeg")
                await callback.message.answer_photo(
                    photo=photo,
                    caption=f"🎉 Поздравляем! Вы нашли {amount} единиц зерна! 🌾\n📦 Текущие запасы: {grain_str} ✅",
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Ошибка при отправке фото: {e}")
                await callback.message.answer(
                    text=f"🎉 Поздравляем! Вы нашли {amount} единиц зерна! 🌾\n📦 Текущие запасы: {grain_str} ✅",
                    parse_mode="HTML"
                )

        # Сбрасываем текущее действие после награды
        set_current_action(user_id, "0")

    elif which_answer == "wrong":
        await callback.message.edit_text(
            text=f"❌ Неверно!\n\n💡 Пояснение:\n{explanation}\n\n✅ Правильный ответ:\n{answer}",
            parse_mode="HTML"
        )
        print(f"Пользователь {user_id} ❌ неверно ответил на вопрос: {question_id}")
        set_current_action(user_id, "0")

    await callback.answer()

async def main():
    init_db()
    init_questions_db()
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())