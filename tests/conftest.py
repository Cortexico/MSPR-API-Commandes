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

TEST_DATABASE_URL = DATABASE_URL

# Create a new engine and session for testing
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

# Override the get_db dependency to use the test database
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Fixture to initialize the database
@pytest_asyncio.fixture(scope='session')
async def initialize_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop tables after tests are done
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

# Fixture for the event loop
@pytest.fixture(scope='function')
def anyio_backend():
    return 'asyncio'

# Fixture for the HTTP client
@pytest_asyncio.fixture(scope='function')
async def client(initialize_database):
    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c
