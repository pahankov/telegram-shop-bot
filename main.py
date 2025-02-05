import logging
from utils.logger import setup_logging

# Инициализация логов должна быть ПЕРВОЙ
setup_logging()

# Затем импортируем остальные модули
from telegram.ext import Application
from config import Config
from handlers.start import start_handler
from handlers.menu import setup_menu_handlers
from database.models import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async def setup_webhook(application):
    # Настройка CloudPub через CLI
    try:
        import subprocess
        subprocess.run([
            "clo", "publish",
            "https", str(Config.WEBHOOK_PORT),
            "--name", Config.WEBHOOK_NAME,
            "--auth", "none"
        ], check=True)
    except Exception as e:
        logging.error(f"CloudPub error: {e}")
        raise

    # Инициализация БД
    engine = create_async_engine(Config.DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Установка вебхука
    await application.bot.set_webhook(f"{Config.CLOUDPUB_SERVER}/{Config.WEBHOOK_NAME}")

def main():
    application = Application.builder().token(Config.TOKEN).post_init(setup_webhook).build()
    application.add_handler(start_handler)
    setup_menu_handlers(application)
    application.run_webhook(
        listen="0.0.0.0",
        port=Config.WEBHOOK_PORT,
        webhook_url=f"{Config.CLOUDPUB_SERVER}/{Config.WEBHOOK_NAME}",
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
