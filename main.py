import logging
import subprocess
from pathlib import Path
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from config import Config
from handlers.start import start_handler
from handlers.menu import setup_menu_handlers
from utils.logger import setup_logging
from database.models import Base
from sqlalchemy.ext.asyncio import create_async_engine

# Инициализация логов
setup_logging()
logger = logging.getLogger("server")


async def setup_webhook(application: Application):
    """Настройка вебхука и БД"""
    try:
        # Публикация через CloudPub
        subprocess.run(
            ["clo", "publish", "https", "8443",
             "--name", "telegram-shop-bot",
             "--auth", "none"],
            check=True,
            shell=True
        )

        # Инициализация БД
        engine = create_async_engine(Config.DB_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await application.bot.set_webhook(Config.WEBHOOK_URL)
        logger.info(f"Webhook: {Config.WEBHOOK_URL}")

    except Exception as e:
        logger.critical(f"Ошибка инициализации: {str(e)}", exc_info=True)
        raise


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}", exc_info=True)
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Произошла ошибка. Попробуйте позже."
        )


def main():
    """Запуск бота"""
    try:
        application = Application.builder().token(Config.TOKEN).post_init(setup_webhook).build()
        application.add_handler(start_handler)
        setup_menu_handlers(application)
        application.add_error_handler(error_handler)

        application.run_webhook(
            listen="0.0.0.0",
            port=8443,
            webhook_url=Config.WEBHOOK_URL,
            drop_pending_updates=True
        )

    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()