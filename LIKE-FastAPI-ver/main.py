from fastapi import FastAPI
import datetime
from pymongo import MongoClient

app = FastAPI()
client = MongoClient("localhost", 27017)
db = client["diary"]

@app.post("/diary/{day}/{name}/{text}")
def make_diary(day: str, name: str, text: str, q: str = None):
    post_time = datetime.date.today().isoformat()
    return {"day": day, "name": name, "text": text, "post-time": post_time, "q": q}


@app.get("/daiary/{item-id}")
def get_diary(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/diaries")
def get_diaries():
    return db["diary"].find_one()
