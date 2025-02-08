from telegram.ext import BasePersistence
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import Config

class StoreData:
    def __init__(self):
        self.callback_data = True
        self.chat_data = True
        self.user_data = True
        self.bot_data = True
        self.conversations = True

class CustomPersistence(BasePersistence):
    """Пользовательский класс для управления сессиями SQLAlchemy"""

    def __init__(self):
        self.engine = create_async_engine(Config.DB_URL)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.store_data = StoreData()  # Используем объект вместо словаря

    async def __aenter__(self):
        self.session = self.async_session()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_session(self):
        async with self.async_session() as session:
            yield session

    async def get_chat_data(self):
        return {}

    async def get_user_data(self):
        return {}

    async def get_bot_data(self):
        return {}

    async def get_conversations(self, name):
        return {}

    async def get_callback_data(self):
        return {}

    async def update_chat_data(self, chat_id, data):
        pass

    async def update_user_data(self, user_id, data):
        pass

    async def update_bot_data(self, data):
        pass

    async def update_conversation(self, name, key, new_state):
        pass

    async def update_callback_data(self, chat_id, callback_id, data):
        pass

    async def flush(self):
        pass

    async def drop_chat_data(self, chat_id):
        pass

    async def drop_user_data(self, user_id):
        pass

    async def refresh_chat_data(self, chat_id, data):
        pass

    async def refresh_user_data(self, user_id, data):
        pass

    async def refresh_bot_data(self, data):
        pass
