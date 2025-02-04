import pytest
from telegram import Update
from telegram.ext import CallbackContext


@pytest.mark.asyncio
async def test_start_command():
    from handlers.start import start
    update = Update(...)  # Создайте mock объект
    context = CallbackContext(...)

    await start(update, context)
    assert "Добро пожаловать" in update.message.text
