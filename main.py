from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

Mongo_URI = os.getenv("Mongo_URI")
client = AsyncIOMotorClient(Mongo_URI)
db = client["Testing"]
testing_col = db["Testing_col"]

app = FastAPI()

class Testing_data(BaseModel):
    name: str
    phone: int
    city: str
    course: str

@app.post("/mongo/insert")
async def mongo_data_insert_helper(data: Testing_data):
    result = await testing_col.insert_one(data.dict())
    return str(result.inserted_id)

def testing_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/mongo/getdata")
async def get_testing_data():
    iterms = []
    cursor = testing_col.find({})
    async for document in cursor:
        iterms.append(testing_helper(document))
    return iterms

@app.get("/mongo/showdata")
async def show_testing_data():
    iterms = []
    cursor = testing_col.find({})
    async for document in cursor:
        iterms.append(testing_helper(document))
    return iterms