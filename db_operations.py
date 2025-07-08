import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            race TEXT DEFAULT '0',
            is_race_selected TEXT DEFAULT '❌ нет',
            current_action TEXT DEFAULT '0',
            current_position TEXT DEFAULT '🏰 колония'
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('users.db')
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
    conn = sqlite3.connect('users.db')
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
    conn = sqlite3.connect('users.db')
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
    conn = sqlite3.connect('users.db')
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
    conn = sqlite3.connect('users.db')
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
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET current_action = ? WHERE id = ?', (action, user_id))
        conn.commit()
        print(f'Пользователь {user_id} выбрал действие: {action}')
    except Exception as e:
        logger.error(f'Ошибка при обновлении current_action для {user_id}: {e}')
    finally:
        conn.close()

def get_current_action(user_id):
    conn = sqlite3.connect('users.db')
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
    conn = sqlite3.connect('users.db')
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
    conn = sqlite3.connect('users.db')
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