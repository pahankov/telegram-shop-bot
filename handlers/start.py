from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.crud import get_or_create_user
from utils.logger import user_logger  # Теперь импорт корректен


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        user = update.effective_user
        async with context.application.persistence.session() as session:
            db_user = await get_or_create_user(session, user)

        greeting = (
            f"Привет, {user.full_name}!"
            if db_user.is_known
            else "Добро пожаловать! Для работы мне потребуется сохранять ваши данные."
        )

        await update.message.reply_text(greeting)
        user_logger.info(f"Новый пользователь: ID={user.id}, Username=@{user.username}")

    except Exception as e:
        user_logger.error(f"Ошибка в /start: {str(e)}", exc_info=True)
        raise


start_handler = CommandHandler('start', start)
