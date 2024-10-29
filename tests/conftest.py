import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the DATABASE_URL to the test database URL before importing app modules
os.environ['DATABASE_URL'] = "postgresql+asyncpg://orders:apiOrders@localhost:5432/orders_db"

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.database import Base, get_db, engine

# Create the tables in the test database
@pytest.fixture(scope='session', autouse=True)
def create_test_database():
    import asyncio
    async def create_tables():
        async with engine.begin() as conn:
            # Corrected line: pass the method without calling it
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_tables())

@pytest_asyncio.fixture(scope="function")
async def async_db():
    async with AsyncSession(engine) as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(async_db):
    # Override get_db dependency
    async def override_get_db():
        async with AsyncSession(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
