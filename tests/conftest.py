import sys
import os
import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, DATABASE_URL
from app.main import app
from app.models import Customer, Product  # Import des modèles nécessaires
from httpx import AsyncClient, ASGITransport

# Configuration de la base de données de test en utilisant aiosqlite
os.environ["IS_TESTING"] = "True"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

# Supprimer le fichier de base de données de test s'il existe déjà
if os.path.exists("./test.db"):
    os.remove("./test.db")

# Utiliser un moteur asynchrone pour les tests
test_engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


# Créer un nouvel event loop pour le module
@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Fonction asynchrone pour créer les tables et ajouter un client et un produit par défaut
async def async_create_all():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Ajouter un client et un produit par défaut pour les tests
    async with TestingSessionLocal() as session:
        # Créer un client par défaut
        new_customer = Customer(name="Test Customer", email="test_customer@example.com", address="123 Test Street")
        session.add(new_customer)
        
        # Créer un produit par défaut
        new_product = Product(id="test_product", name="Test Product", description="A product for testing", price=99.99, stock=10)
        session.add(new_product)
        
        await session.commit()


# Fonction asynchrone pour supprimer les tables
async def async_drop_all():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Surcharger la dépendance get_db pour utiliser la session de test
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


# Fixture pour préparer et nettoyer la base de données de test
@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    await async_create_all()
    yield
    await async_drop_all()


# Fixture pour le client asynchrone
@pytest_asyncio.fixture(scope="module")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
