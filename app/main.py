from fastapi import FastAPI
from app.routers import orders
from app.database import create_tables
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from app.rabbitmq_consumer_clients import start_customer_consumer
from app.rabbitmq_consumer_produits import start_product_consumer
import asyncio
from app.routers.orders import router as orders_router, customer_router

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_tables()
    asyncio.create_task(start_customer_consumer())
    asyncio.create_task(start_product_consumer())
    yield
    # Shutdown code (if any)

app = FastAPI(lifespan=lifespan)

app.include_router(orders.router)
app.include_router(customer_router)
