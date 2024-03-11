from sqlalchemy import DateTime, Float, String, Text, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Application(Base):
    __tablename__ = 'application'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_article: Mapped[int] = mapped_column(Integer, nullable=False)
    message_for_mailing: Mapped[str] = mapped_column(String(256), nullable=False)
