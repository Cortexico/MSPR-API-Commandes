import sys
import os

# Ajouter le répertoire racine du projet à sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Configuration du moteur de base de données asynchrone
engine = create_async_engine(DATABASE_URL, echo=False)

# Configuration de la session de base de données asynchrone
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

# Fixture pour la base de données
@pytest_asyncio.fixture(scope="function")
async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Fixture pour le client asynchrone
@pytest_asyncio.fixture(scope="function")
async def client(async_db):
    # Remplacer la dépendance get_db par la session de test
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
