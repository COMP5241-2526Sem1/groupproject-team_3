from config import Config
from pymongo import MongoClient

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

act = db.activities.find_one({'title': 'Understanding AI-Assisted Coding in Integrated Development Environments'})

if act:
    print(f"Title: {act['title']}")
    print(f"Deadline: {act.get('deadline')}")
    print(f"Created at: {act.get('created_at')}")
else:
    # Search for similar
    acts = list(db.activities.find({'title': {'$regex': 'Understanding', '$options': 'i'}}).limit(3))
    print(f"Found {len(acts)} activities:")
    for a in acts:
        print(f"  - {a['title']}")
        print(f"    Deadline: {a.get('deadline')}")
