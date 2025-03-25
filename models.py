from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class HistoryModel(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str]
    date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))