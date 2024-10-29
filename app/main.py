from fastapi import FastAPI
from app.routers import orders
from app.database import create_tables
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.include_router(orders.router)

# Create tables at application startup
@app.on_event("startup")
async def startup_event():
    await create_tables()
