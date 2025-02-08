from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
from utils.logger import server_logger

buttons = [
    ["Оценить нас", "Вакансии"],
    ["Связь с АДМ", "Выгодные предложения"]
]

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=markup)
    server_logger.info(f"Меню отображено для пользователя: {update.effective_user.id}")

def setup_menu_handlers(application):
    application.add_handler(MessageHandler(filters.Text(["Оценить нас"]), rate_us))
    application.add_handler(MessageHandler(filters.Text(["Вакансии"]), vacancies))
    application.add_handler(MessageHandler(filters.Text(["Связь с АДМ"]), contact_admin))
    application.add_handler(MessageHandler(filters.Text(["Выгодные предложения"]), special_offers))

# Обработчики кнопок
async def rate_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Наша оценка на маркетплейсах: 5/5 ★")
    server_logger.info(f"Команда 'Оценить нас' выполнена для пользователя: {update.effective_user.id}")

async def vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Актуальные вакансии: ...")
    server_logger.info(f"Команда 'Вакансии' выполнена для пользователя: {update.effective_user.id}")

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Свяжитесь с @admin")
    server_logger.info(f"Команда 'Связь с АДМ' выполнена для пользователя: {update.effective_user.id}")

async def special_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Специальные предложения этой недели: ...")
    server_logger.info(f"Команда 'Выгодные предложения' выполнена для пользователя: {update.effective_user.id}")
