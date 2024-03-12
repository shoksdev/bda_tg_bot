from sqlalchemy import DateTime, String, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовая модель"""

    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Application(Base):
    """Модель заявок, храним имя пользователя, артикул товара и сообщение, которое нужно вывести с рассылкой"""

    __tablename__ = 'application'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_article: Mapped[int] = mapped_column(Integer, nullable=False)
    message_for_mailing: Mapped[str] = mapped_column(String(256), nullable=False)
