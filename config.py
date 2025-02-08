import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Обязательные параметры
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("Токен бота не указан в .env")

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    if not WEBHOOK_URL:
        raise ValueError("WEBHOOK_URL не указан в .env")

    # Порт для вебхука (смените порт на другой, который свободен)
    WEBHOOK_PORT = 8444  # Попробуйте использовать другой порт

    # Режим отладки
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # База данных
    DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///shop_bot.db")

    # Логирование
    LOGS_DIR = "logs"
    SERVER_LOG = Path(LOGS_DIR) / "server.log"
    USER_LOG = Path(LOGS_DIR) / "user_actions.log"
