"""
检查数据库中poll活动的实际数据结构
"""
from services.db_service import db_service
import json

print("=" * 80)
print("检查所有Poll类型的活动")
print("=" * 80)

# Ensure connection
db_service._connect()

# Find all poll activities
activities = list(db_service._db.activities.find({'type': 'poll'}).sort('created_at', -1).limit(5))

for i, activity in enumerate(activities, 1):
    print(f"\n活动 #{i}: {activity.get('title')}")
    print(f"ID: {activity['_id']}")
    print(f"类型: {activity.get('type')}")
    print(f"创建时间: {activity.get('created_at')}")
    print(f"AI生成: {activity.get('ai_generated', False)}")
    
    content = activity.get('content', {})
    print(f"\nContent keys: {list(content.keys())}")
    
    # Check if it has 'questions' (multi-question format)
    if 'questions' in content:
        questions = content['questions']
        print(f"✅ 有 'questions' 字段 (多问题格式)")
        print(f"问题数量: {len(questions)}")
        
        # Show first question details
        if questions:
            first_q = questions[0]
            print(f"\n第一个问题的结构:")
            print(json.dumps(first_q, indent=2, ensure_ascii=False))
    
    # Check if it has 'question' (single-question format)
    if 'question' in content:
        print(f"✅ 有 'question' 字段 (单问题格式)")
        print(f"问题内容: {content['question'][:100]}...")
        print(f"选项数量: {len(content.get('options', []))}")
    
    print("-" * 80)

print("\n完成!")
