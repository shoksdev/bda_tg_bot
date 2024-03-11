from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Application


async def orm_add_application(session: AsyncSession, user_id: int, product_article: int):
    obj = Application(
        user_id=user_id,
        product_article=product_article,
    )
    session.add(obj)
    await session.commit()


async def orm_get_applications(session: AsyncSession):
    query = select(Application)
    result = await session.execute(query)
    return result.scalars().all()
