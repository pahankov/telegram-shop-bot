import logging
from pathlib import Path
from config import Config

# Инициализируем логгеры на уровне модуля
server_logger = logging.getLogger("server")
user_logger = logging.getLogger("user")


def setup_logging():
    # Создаем папку для логов
    Path("logs").mkdir(exist_ok=True)

    # Форматтер для логов
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Обработчики для серверных логов
    server_handler = logging.FileHandler(Config.SERVER_LOG_PATH)
    server_handler.setFormatter(formatter)
    server_logger.addHandler(server_handler)
    server_logger.setLevel(logging.INFO)

    # Обработчики для пользовательских логов
    user_handler = logging.FileHandler(Config.USER_LOG_PATH)
    user_handler.setFormatter(formatter)
    user_logger.addHandler(user_handler)
    user_logger.setLevel(logging.INFO)
