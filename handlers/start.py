async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await get_or_create_user(user)

    if not db_user.is_known:
        # Запрос разрешений
        await update.message.reply_text(
            "Для продолжения работы нам нужно сохранить ваши базовые данные.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Разрешить", callback_data="accept_terms"),
                 InlineKeyboardButton("Отказать", callback_data="decline_terms")]
            ])
        )
    else:
        await update.message.reply_text(f"С возвращением, {user.full_name}!")


async def handle_terms_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "accept_terms":
        # Обновляем статус пользователя
        await update_user_status(query.from_user.id, is_known=True)
        await query.edit_message_text("Спасибо! Теперь вы можете пользоваться ботом.")
    else:
        await query.edit_message_text("Без сохранения данных функционал бота будет ограничен.")
