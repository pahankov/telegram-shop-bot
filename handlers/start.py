from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.crud import get_or_create_user
from utils.logger import user_logger  # Теперь импорт будет работать


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    async with context.application.persistence.session() as session:
        db_user = await get_or_create_user(session, user)

    greeting = f"Привет, {user.full_name}!" if db_user.is_known else """
    Добро пожаловать! Для работы мне потребуется сохранять ваши данные.
    """

    await update.message.reply_text(greeting)
    user_logger.info(f"User {user.id} started conversation")


start_handler = CommandHandler('start', start)
