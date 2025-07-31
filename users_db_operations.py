import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            race TEXT DEFAULT '0',
            is_race_selected TEXT DEFAULT '❌ нет',
            current_action TEXT DEFAULT '0',
            current_position TEXT DEFAULT '🏰 колония',
            question_id INTEGER DEFAULT 0,
            grain_storage TEXT DAFAULT "0/10",
            all_collecting_bonus INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (id, race) VALUES (?, 0)', (user_id,))
        conn.commit()
        print(f'Пользователь {user_id} добавлен')
    else:
        print(f'Пользователь {user_id} уже есть в базе')
    conn.close()


def set_race(user_id, race):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET race = ? WHERE id = ?', (race, user_id))
        conn.commit()
        print(f"Пользователь {user_id} изучает рассу: {get_race(user_id)}")
    except Exception as e:
        logger.error(f'Ошибка при обновлении race для {user_id}: {e}')
    finally:
        conn.close()


def get_race(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT race FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f'Ошибка при получении race для {user_id}: {e}')
        return None
    finally:
        conn.close()

def set_is_race_selected(user_id, a):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET is_race_selected = ? WHERE id = ?', (a, user_id))
        conn.commit()
        print(f"Пользователь {user_id} выбрал расу: {get_race(user_id)}")
    except Exception as e:
        logger.error(f'Ошибка при обновлении is_race_selected для {user_id}: {e}')
    finally:
        conn.close()

def get_is_race_selected(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT is_race_selected FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f'Ошибка при получении is_race_selected для {user_id}: {e}')
        return None
    finally:
        conn.close()

def set_current_action(user_id, action):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET current_action = ? WHERE id = ?', (action, user_id))
        conn.commit()
        if action != "0":
            print(f'Пользователь {user_id} выбрал действие: {action}')
    except Exception as e:
        logger.error(f'Ошибка при обновлении current_action для {user_id}: {e}')
    finally:
        conn.close()

def get_current_action(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT current_action FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f'Ошибка при получении current_action для {user_id}: {e}')
        return None
    finally:
        conn.close()

def set_current_position(user_id, position):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET current_position = ? WHERE id = ?', (position, user_id))
        conn.commit()
        print(f'Пользователь {user_id} переместился в {position}')
    except Exception as e:
        logger.error(f'Ошибка при обновлении current_position для {user_id}: {e}')
    finally:
        conn.close()

def get_current_position(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT current_position FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f'Ошибка при получении current_position для {user_id}: {e}')
        return None
    finally:
        conn.close()

def set_question_id(user_id, question_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET question_id = ? WHERE id = ?', (question_id, user_id))
        conn.commit()
        if question_id != 0:
            print(f"Пользователь {user_id} отвечает на вопрос: {question_id}")
    except Exception as e:
        logger.error(f'Ошибка при обновлении question_id для {user_id}: {e}')
    finally:
        conn.close()

def get_question_id(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT question_id FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f'Ошибка при получении question_id для {user_id}: {e}')
        return None
    finally:
        conn.close()


def set_grain_storage(user_id, current_amount=None, max_capacity=None):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        # Получаем текущие значения
        cursor.execute('SELECT grain_storage FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()

        # Парсим существующие значения или устанавливаем по умолчанию
        if result and result[0]:
            existing_current, existing_max = map(int, result[0].split('/'))
        else:
            existing_current, existing_max = 0, 10  # Значения по умолчанию

        # Обновляем только указанные параметры
        new_current = existing_current if current_amount is None else current_amount
        new_max = existing_max if max_capacity is None else max_capacity

        # Проверяем, чтобы текущее количество не превышало максимальное
        if new_current > new_max:
            new_current = new_max

        # Формируем строку хранилища
        storage_str = f"{new_current}/{new_max}"

        # Обновляем значение в базе
        cursor.execute('UPDATE users SET grain_storage = ? WHERE id = ?', (storage_str, user_id))
        conn.commit()
        logger.info(f"Для пользователя {user_id} установлено хранилище: {storage_str}")
        return storage_str

    except Exception as e:
        logger.error(f'Ошибка при установке grain_storage для {user_id}: {e}')
        return None
    finally:
        conn.close()


def get_grain_storage(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT grain_storage FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()

        if result and result[0]:
            current, max_capacity = map(int, result[0].split('/'))
            return current, max_capacity, result[0]
        else:
            # Возвращаем значения по умолчанию (0/10)
            return 0, 10, "0/10"

    except Exception as e:
        logger.error(f'Ошибка при получении grain_storage для {user_id}: {e}')
        return 0, 10, "0/10"  # Возвращаем дефолтные значения при ошибке
    finally:
        conn.close()

def set_all_collecting_bonus(user_id, bonus):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET all_collecting_bonus = ? WHERE id = ?', (bonus, user_id))
        conn.commit()
        print(f"Бонус для сбора всех ресурсов у {user_id} установлен на: {bonus}")
    except Exception as e:
        logger.error(f'Ошибка при обновлении all_collecting_bonus для {user_id}: {e}')
    finally:
        conn.close()

def get_all_collecting_bonus(user_id):
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT all_collecting_bonus FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f'Ошибка при получении all_collecting_bonus для {user_id}: {e}')
        return None
    finally:
        conn.close()