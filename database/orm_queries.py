from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Application


async def orm_add_application(session: AsyncSession, data: dict):
    obj = Application(
        user_id=data.get('user_id'),
        product_article=int(data.get('product_article')),
    )
    session.add(obj)
    await session.commit()