from fastapi import FastAPI
from app.routers import orders
from app.database import create_tables
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

app.include_router(orders.router)

# Créer les tables au démarrage de l'application
@app.on_event("startup")
async def startup_event():
    await create_tables()
