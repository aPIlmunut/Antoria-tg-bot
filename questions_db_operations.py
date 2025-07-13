import sqlite3
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_questions_db():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            subject TEXT DEFAULT '0',
            question TEXT DEFAULT '0',
            explanation TEXT DEFAULT '0',
            answer TEXT DEFAULT '0',
            first_wrong_answer TEXT DEFAULT '0',
            second_wrong_answer TEXT DEFAULT '0'
        )
    ''')
    conn.commit()
    conn.close()


def get_random_question_by_subject(subject):
    """
    Возвращает случайный вопрос, правильный ответ, два неправильных ответа и объяснение по указанному предмету

    :param subject: Название предмета для фильтрации вопросов
    :return: Кортеж (question, answer, first_wrong_answer, second_wrong_answer, explanation)
             или None, если вопросы не найдены
    """
    try:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()

        # Получаем все данные вопроса по предмету
        cursor.execute('''
            SELECT question, answer, first_wrong_answer, second_wrong_answer, explanation 
            FROM questions 
            WHERE subject = ?
        ''', (subject,))

        questions = cursor.fetchall()

        if not questions:
            logger.warning(f"❌ Вопросы для предмета: {subject} не найдены")
            return None

        # Выбираем случайный вопрос
        random_question = random.choice(questions)
        return random_question

    except sqlite3.Error as e:
        logger.error(f"❌ Ошибка базы данных вопросов: {e}")
        return None
    finally:
        if conn:
            conn.close()
