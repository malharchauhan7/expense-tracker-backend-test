from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb://localhost:27017"
client = AsyncIOMotorClient(uri)

db = client["expense-tracker-testing"]

users_collection = db["users"]
transactions_collection = db["transactions"]
category_collection = db["category"]