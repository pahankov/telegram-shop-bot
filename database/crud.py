from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User


async def get_or_create_user(session: AsyncSession, tg_user) -> User:
    """Получает или создает пользователя в БД"""
    try:
        result = await session.execute(select(User).where(User.chat_id == tg_user.id))
        user = result.scalars().first()

        if not user:
            user = User(
                chat_id=tg_user.id,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user

    except Exception as e:
        await session.rollback()
        raise
