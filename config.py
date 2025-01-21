import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Чтение токена из переменной окружения
TOKEN = os.getenv('BOT_TOKEN')
USDA_KEY = os.getenv('USDA_KEY')
OPEN_W_KEY = os.getenv('OPEN_W_KEY')
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
if not USDA_KEY:
    raise ValueError("Переменная окружения USDA_KEY не установлена!")
if not USDA_KEY:
    raise ValueError("Переменная окружения OPEN_W_KEY не установлена!")