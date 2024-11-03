import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from app.database import Base, get_db, DATABASE_URL
from app.main import app
from httpx import AsyncClient, ASGITransport

# Utilisation d'une URL pour la base de données de test
TEST_DATABASE_URL = DATABASE_URL + "_test"

# Configuration de l'engine pour la base de données de test
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


# Fonction pour créer la base de données de test si elle n'existe pas
async def create_test_database():
    async with create_async_engine(DATABASE_URL).begin() as conn:
        try:
            await conn.execute(f"CREATE DATABASE {TEST_DATABASE_URL.rsplit('/', 1)[-1]}")
        except ProgrammingError:
            # La base de données existe déjà
            pass


# Surcharge de la dépendance `get_db` pour utiliser la session de test
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope='function', autouse=True)
async def initialize_database():
    # Créer la base de données de test si elle n'existe pas
    await create_test_database()
    # Créer les tables pour les tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Supprimer les tables après les tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
