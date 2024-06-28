from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.settings import MONGODB_URL
from app.models import user as UserModel
from app.models import booking as BookingModel

db_module = APIRouter()
async def init():
    # client = AsyncIOMotorClient("mongodb+srv://mahmud:<password>@cluster0.5iguurt.mongodb.net/?appName=Cluster0")
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client.get_database("Cluster0") # Cluster0 is database/Cluster name from mongodb
    await init_beanie(database, document_models=[UserModel.User, BookingModel.Booking])

@db_module.on_event("startup")
async def on_startup():
    await init()

