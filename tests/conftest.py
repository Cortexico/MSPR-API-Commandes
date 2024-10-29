import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, DATABASE_URL
from app.main import app
from httpx import AsyncClient

# Create a new engine and session for testing
test_engine = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

# Override the get_db dependency
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Create the tables before running tests
@pytest.fixture(scope='session', autouse=True)
async def initialize_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_engine.dispose()

@pytest_asyncio.fixture(scope='function')
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
