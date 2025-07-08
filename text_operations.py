import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_text(filename):
    try:
        with open(f"texts/{filename}", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Файл с текстом не найден: {filename}")
        return f"❌ Текст не загружен ({filename})"