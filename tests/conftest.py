import sys
import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, DATABASE_URL
from app.main import app
from httpx import AsyncClient, ASGITransport

# Utilisation d'une URL de base de données dédiée aux tests
TEST_DATABASE_URL = DATABASE_URL + "_test"  # Ajouter _test pour éviter les conflits
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


# Surcharge de la dépendance `get_db` pour utiliser la session de test
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


# Création et suppression des tables avant et après chaque test
@pytest_asyncio.fixture(scope='function', autouse=True)
async def initialize_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Configuration de la fixture pour le client HTTP asynchrone
@pytest_asyncio.fixture(scope='function')
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
