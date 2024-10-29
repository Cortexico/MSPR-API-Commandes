import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()  # This will not override existing environment variables

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

# Function to create tables at startup
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db():
    async with async_session() as session:
        yield session
