from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
from handlers.start import start_handler
from handlers.menu import setup_menu_handlers
import logging
from utils.logger import setup_logging


async def post_init(application):
    await application.bot.set_webhook(Config.WEBHOOK_URL)


def main():
    setup_logging()
    application = Application.builder().token(Config.TOKEN).post_init(post_init).build()

    # Регистрация обработчиков
    application.add_handler(start_handler)
    setup_menu_handlers(application)

    # Настройка вебхука
    application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        webhook_url=Config.WEBHOOK_URL
    )


if __name__ == "__main__":
    main()