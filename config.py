import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Основные настройки
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    SERVER_LOG_PATH = "logs/server.log"
    USER_LOG_PATH = "logs/user_actions.log"

    # Настройки CloudPub
    CLOUDPUB_SERVER = "https://cloudpub.ru"
    CLOUDPUB_TOKEN = os.getenv("CLOUDPUB_TOKEN")
    WEBHOOK_PORT = 8443
    WEBHOOK_NAME = "telegram-shop-bot"

    # Настройки БД
    DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///shop_bot.db")
