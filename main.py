import datetime

import motor.motor_asyncio
from fastapi import FastAPI

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongo", 27017, username="root", password="example"
)
db = client.get_database("diary")
collection = db.get_collection("diary")


@app.post("/diary/{day}/{name}/{text}")
async def make_diary(day: str, name: str, text: str, q: str = None):
    post_time = datetime.date.today().isoformat()
    diary = {"day": day, "name": name, "text": text, "post-time": post_time}
    try:
        await collection.insert_one(diary)
        return {"diary": diary, "q": q}
    except Exception as e:
        return {"error": str(e)}


@app.get("/diary/{item-id}")
async def get_diary(item_id: str, q: str = None):
    diary = await collection.find_one({"_id": item_id})
    return {"diary": diary, "q": q}


@app.get("/diaries")
async def get_diaries():
    diaries = []
    cursor = collection.find({})
    for diary in await cursor.to_list(length=100):
        diary["_id"] = str(diary["_id"])
        diaries.append(diary)
    return {"diaries": diaries}
