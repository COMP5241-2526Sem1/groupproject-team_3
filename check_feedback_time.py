"""Check feedback_at timestamps in database"""
from config import Config
from pymongo import MongoClient

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Find activities with feedback
activities = list(db.activities.find(
    {'responses.feedback': {'$exists': True}},
    {'title': 1, 'responses': 1}
).limit(5))

print("Activities with feedback:")
for activity in activities:
    responses_with_feedback = [r for r in activity.get('responses', []) if r.get('feedback')]
    if responses_with_feedback:
        print(f"\n活动: {activity.get('title')}")
        for resp in responses_with_feedback:
            print(f"  学生: {resp.get('student_name', 'Unknown')}")
            print(f"  Feedback: {resp.get('feedback', '')[:50]}...")
            print(f"  feedback_at: {resp.get('feedback_at')}")
