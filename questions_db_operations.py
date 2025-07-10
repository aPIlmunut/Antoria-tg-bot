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
            answer TEXT DEFAULT '0'
        )
    ''')
    conn.commit()
    conn.close()


def get_random_question_by_subject(subject):
    try:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()

        # Сначала получаем все вопросы по предмету
        cursor.execute('''
            SELECT question, answer FROM questions 
            WHERE subject = ?
        ''', (subject,))

        questions = cursor.fetchall()

        if not questions:
            logger.warning(f"No questions found for subject: {subject}")
            return None

        # Выбираем случайный вопрос
        random_question = random.choice(questions)
        return random_question

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()
