from pymongo.mongo_client import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)

db = client["expense-tracker-testing"]

users_collection = db["users"]