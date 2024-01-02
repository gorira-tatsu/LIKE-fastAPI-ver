from fastapi import FastAPI
import datetime
import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongo", 27017, username="root", password="example")
db = client.get_database("diary")
collection = db.get_collection("diary")

@app.post("/diary/{day}/{name}/{text}")
async def make_diary(day: str, name: str, text: str, q: str = None):
    post_time = datetime.date.today().isoformat()
    diary = {"day": day, "name": name, "text": text, "post-time": post_time}
    await collection.insert_one(diary)
    return {"day": day, "name": name, "text": text, "post-time": post_time, "q": q}


@app.get("/daiary/{item-id}")
def get_diary(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/diaries")
async def get_diaries():
    diaries = []
    cursor = collection.find({})
    for diary in await cursor.to_list(length=100):
        diary["_id"] = str(diary["_id"])
        diaries.append(diary)
    return {"diaries": diaries}