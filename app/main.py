from fastapi import FastAPI
from app.routers import orders
from app.database import create_tables
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(lifespan=lifespan)

app.include_router(orders.router)
