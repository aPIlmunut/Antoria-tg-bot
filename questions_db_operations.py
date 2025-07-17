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
            id INTEGER PRIMARY KEY,
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
    try:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()

        # Получаем все данные вопроса по предмету
        cursor.execute('''
            SELECT question, id , answer, first_wrong_answer, second_wrong_answer 
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

def get_explanation_and_answer_by_id(question_id):
    try:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()

        # Получаем объяснение и правильный ответ по ID вопроса
        cursor.execute('''
            SELECT explanation, answer 
            FROM questions 
            WHERE id = ?
        ''', (question_id,))

        result = cursor.fetchone()

        if not result:
            logger.warning(f"❌ Вопрос с ID: {question_id} не найден")
            return None, None

        explanation, answer = result
        return explanation, answer

    except sqlite3.Error as e:
        logger.error(f"❌ Ошибка базы данных при получении объяснения и ответа: {e}")
        return None, None
    finally:
        if conn:
            conn.close()
