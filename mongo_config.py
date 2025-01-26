import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO = os.getenv("MONGO")

client = pymongo.MongoClient(MONGO)
dnd = client["dnd_database"]
characters = dnd["characters"]
classes = dnd["classes"]
races = dnd["races"]
