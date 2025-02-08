import logging
from pathlib import Path
from config import Config

# Глобальные логгеры
server_logger = logging.getLogger("server")
user_logger = logging.getLogger("user")


def setup_logging():
    """Инициализация системы логирования"""
    try:
        # Создание папки для логов
        Path(Config.LOGS_DIR).mkdir(parents=True, exist_ok=True)

        # Форматтер
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Серверные логи (DEBUG уровень)
        server_handler = logging.FileHandler(Config.SERVER_LOG, encoding='utf-8')
        server_handler.setFormatter(formatter)
        server_logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
        server_logger.addHandler(server_handler)

        # Пользовательские логи (только INFO)
        user_handler = logging.FileHandler(Config.USER_LOG, encoding='utf-8')
        user_handler.setFormatter(formatter)
        user_logger.setLevel(logging.INFO)
        user_logger.addHandler(user_handler)

        # Консольное логирование для DEBUG
        if Config.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            server_logger.addHandler(console_handler)

    except Exception as e:
        logging.critical(f"Ошибка инициализации логов: {str(e)}", exc_info=True)
        raise
