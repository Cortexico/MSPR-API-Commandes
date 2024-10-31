# import os
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv
# from contextlib import asynccontextmanager

# # Load environment variables
# load_dotenv()  # This will not override existing environment variables

# POSTGRES_USER = os.getenv("POSTGRES_USER", "orders")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "apiOrders")
# POSTGRES_DB = os.getenv("POSTGRES_DB", "orders_db")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# engine = create_async_engine(DATABASE_URL, echo=True)

# async_session = sessionmaker(
#     bind=engine, expire_on_commit=False, class_=AsyncSession
# )

# Base = declarative_base()

# from app import models

# # Function to create tables at startup
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# @asynccontextmanager
# async def get_db():
#     async with async_session() as session:
#         yield session

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()  # Cela ne remplacera pas les variables d'environnement existantes

POSTGRES_USER = os.getenv("POSTGRES_USER", "orders")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "apiOrders")
POSTGRES_DB = os.getenv("POSTGRES_DB", "orders_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

from app import models

# Fonction pour créer les tables au démarrage
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Fonction de dépendance pour obtenir une session de base de données
async def get_db():
    async with async_session() as session:
        yield session

