from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Application


async def orm_add_application(session: AsyncSession, user_id: int, product_article: int, message_for_mailing: str):
    """Создаём и применяем запрос на добавление заявки в базу данных"""

    obj = Application(
        user_id=user_id,
        product_article=product_article,
        message_for_mailing=message_for_mailing
    )
    session.add(obj)
    await session.commit()


async def orm_get_applications(session: AsyncSession):
    """Получаем все заявки из базы данных"""

    query = select(Application)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_application(session: AsyncSession, user_id: int, product_article: int):
    """Получаем заявки с указанным пользователем и артикулом товара"""

    query = select(Application).where(Application.user_id == user_id and Application.product_article == product_article)
    result = await session.execute(query)
    return result.scalars().all()
