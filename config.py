import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv("7030286976:AAG5qqKZ6p0KL0x5JssORw7fB7fU762PiUk")
    DB_URL = os.getenv("DATABASE_URL", "sqlite:///shop_bot.db")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    SERVER_LOG_PATH = "logs/server.log"
    USER_LOG_PATH = "logs/user_actions.log"