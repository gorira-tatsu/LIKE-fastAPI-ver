import datetime
from typing import Optional  # 追加

import motor.motor_asyncio
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongo", 27017, username="root", password="example"
)
db = client.get_database("diary")
collection = db.get_collection("diary")


origins = [
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/diary/{day}/{name}/{text}")
async def make_diary(day: str, name: str, text: str, q: Optional[str] = None):  # 修正
    post_time = datetime.date.today().isoformat()
    diary = {"day": day, "name": name, "text": text, "post-time": post_time}
    try:
        await collection.insert_one(diary)
        return {"diary": diary, "q": q}
    except Exception as e:
        return {"error": str(e)}


@app.get("/diary/{item-id}")
async def get_diary(item_id: str, q: Optional[str] = None):  # 修正
    diary = await collection.find_one({"_id": item_id})
    return {"diary": diary, "q": q}


@app.get("/diaries")
async def get_diaries(q: Optional[str] = None):  # 修正
    diaries = []
    cursor = collection.find({})
    for diary in await cursor.to_list(length=100):
        diary["_id"] = str(diary["_id"])
        diaries.append(diary)
    return {"diaries": diaries, "q": q}
