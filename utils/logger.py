import logging
from config import Config

def setup_logging():
    # Серверные логи
    server_logger = logging.getLogger("server")
    server_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(Config.SERVER_LOG_PATH)
    server_logger.addHandler(file_handler)

    # Пользовательские логи
    user_logger = logging.getLogger("user")
    user_logger.setLevel(logging.INFO)
    user_handler = logging.FileHandler(Config.USER_LOG_PATH)
    user_logger.addHandler(user_handler)

def user_logger():
    return logging.getLogger("user")
