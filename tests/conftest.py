import os
import sys
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, DATABASE_URL
from app.main import app
from httpx import AsyncClient, ASGITransport

# Définir une URL de base de données de test distincte
TEST_DATABASE_URL = DATABASE_URL + "_test"

# Créer un moteur pour la base de données de test
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


# Fonction de dépendance pour obtenir la session de test
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

# Remplacer la dépendance de base de données par celle de test
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='function', autouse=True)
async def initialize_database():
    # Créer les tables avant chaque test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Supprimer les tables après chaque test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def client():
    # Initialiser le client asynchrone pour les tests
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
