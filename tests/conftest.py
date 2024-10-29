import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, DATABASE_URL
from app.main import app
from httpx import AsyncClient, ASGITransport

TEST_DATABASE_URL = DATABASE_URL + "_test"

test_engine = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='function', autouse=True)
async def initialize_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop tables and dispose of the engine after each test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest_asyncio.fixture(scope='function')
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
