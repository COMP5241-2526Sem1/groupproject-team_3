from config import Config
from pymongo import MongoClient
from utils.time_utils import get_hk_time

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

act = db.activities.find_one({'title': 'Software Testing Fundamentals Quiz'})

if act:
    print(f"Title: {act['title']}")
    print(f"Deadline: {act.get('deadline')}")
    print(f"Current: {get_hk_time()}")
    print(f"Expired: {get_hk_time() > act.get('deadline')}")
else:
    print("Not found")
