from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import Tron, AsyncTron
from tronpy.providers import AsyncHTTPProvider

from .settings import async_session, get_api_key


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            raise e
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_client() -> Tron:
    async with AsyncTron(AsyncHTTPProvider(
            "https://api.trongrid.io",
            api_key=get_api_key())) as client:
        try:
            yield client
        except Exception as e:
            raise e
        finally:
            await client.close()


ClientDep = Annotated[AsyncTron, Depends(get_client)]
