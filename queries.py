from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import HistoryModel


async def save_request(address: str, session: AsyncSession):
    new_record = HistoryModel(address=address)
    session.add(new_record)
    await session.commit()


async def get_history_query(records: int, session: AsyncSession):
    query = select(HistoryModel).offset(0).limit(records)
    result = await session.execute(query)
    history = result.scalars().all()
    print(history)
    return history
