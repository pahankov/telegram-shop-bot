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
        logs_dir = Path(Config.LOGS_DIR)
        logs_dir.mkdir(parents=True, exist_ok=True)  # Исправлено: 'exist_ok' вместо 'existовать'

        # Форматтер
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Исправлено: 'levelname' вместо 'levellevel'
            datefmt="%Y-%m-%d %H:%M:%S"  # Исправлено: ':%М:%С' на ':%M:%S'
        )

        # Серверные логи
        server_handler = logging.FileHandler(
            str(logs_dir / "server.log"),
            encoding="utf-8",
            mode="w"
        )
        server_handler.setFormatter(formatter)
        server_logger.setLevel(logging.DEBUG)
        server_logger.addHandler(server_handler)

        # Пользовательские логи
        user_handler = logging.FileHandler(
            str(logs_dir / "user_actions.log"),
            encoding="utf-8",
            mode="w"
        )
        user_handler.setFormatter(formatter)
        user_logger.setLevel(logging.INFO)
        user_logger.addHandler(user_handler)

        # Консольное логирование
        if Config.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            server_logger.addHandler(console_handler)

        # Тестовое сообщение
        server_logger.info("Логирование успешно настроено!")
        user_logger.info("Пользовательские логи готовы к записи.")

    except Exception as e:
        print(f"FATAL LOGGING ERROR: {str(e)}")
        raise
