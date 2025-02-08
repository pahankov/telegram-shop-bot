import logging
import tracemalloc  # Импортируем tracemalloc для отладки
import asyncio
import nest_asyncio
import telegram  # Добавляем импорт библиотеки Telegram
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from config import Config
from handlers.start import start_handler
from handlers.menu import setup_menu_handlers, show_menu
from utils.logger import setup_logging
from database.models import Base
from database.persistence import CustomPersistence
from sqlalchemy.ext.asyncio import create_async_engine

# Включаем tracemalloc
tracemalloc.start()

# Инициализация логов
setup_logging()
logger = logging.getLogger("server")

# Применяем патч для вложенного цикла событий
nest_asyncio.apply()


async def setup_webhook(application: Application):
    """Настройка вебхука и БД"""
    try:
        logger.info("Начало настройки вебхука")
        logger.info("Публикация вебхука исключена для отладки")
        logger.info("Инициализация базы данных")

        engine = create_async_engine(Config.DB_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База данных инициализирована")

        while True:
            try:
                await application.bot.set_webhook(Config.WEBHOOK_URL)
                logger.info(f"Webhook установлен: {Config.WEBHOOK_URL}")
                break
            except telegram.error.RetryAfter as e:
                logger.warning(f"Flood control exceeded. Retry in {e.retry_after} seconds")
                await asyncio.sleep(e.retry_after)

    except Exception as e:
        logger.critical(f"Ошибка инициализации: {str(e)}", exc_info=True)
        raise


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}", exc_info=True)
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Произошла ошибка. Попробуйте позже."
        )


async def main():
    """Запуск бота"""
    try:
        logger.info("Начало запуска бота")
        persistence = CustomPersistence()
        application = Application.builder().token(Config.TOKEN).persistence(persistence).post_init(
            setup_webhook).build()
        application.add_handler(start_handler)
        application.add_handler(CommandHandler('menu', show_menu))
        setup_menu_handlers(application)
        application.add_error_handler(error_handler)

        logger.info("Зарегистрированы обработчики")

        await application.run_webhook(
            listen="0.0.0.0",
            port=Config.WEBHOOK_PORT,
            webhook_url=Config.WEBHOOK_URL,
            drop_pending_updates=True
        )
        logger.info("Бот успешно запущен")

    except asyncio.exceptions.CancelledError:
        logger.error("Цикл событий был отменен")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}", exc_info=True)
    finally:
        await application.shutdown()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    # Печатаем статистику tracemalloc
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    logger.info("Топ 10 строк по использованию памяти:")
    for stat in top_stats[:10]:
        logger.info(stat)
