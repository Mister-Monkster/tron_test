import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..main import app


@pytest.fixture(scope="session")
def event_loop():
    """Фикстура для создания event loop с правильным scope"""
    import asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def async_engine():
    """Фикстура для асинхронного движка БД"""
    engine = create_async_engine(
        "postgresql+asyncpg://user:password@localhost/testdb",
        echo=False,
        pool_size=5,
        max_overflow=10
    )
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def async_session_maker(async_engine):
    """Фикстура для фабрики асинхронных сессий"""
    return sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

@pytest.fixture
async def db_session(async_session_maker):
    """Фикстура для отдельных тестовых сессий"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@pytest.mark.asyncio
async def test_get_history():
    async with (AsyncClient(
            transport=ASGITransport(app=app),
                           base_url='http://test') as ac):
        response = await ac.get('/get-history')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_info():
    async with AsyncClient(
            transport=ASGITransport(app=app),
                           base_url='http://test') as ac:
        response = await ac.post('/get-info', json={"address": "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL"},
                                 headers={"Content-Type": "application/json"})
        assert response.status_code == 200
