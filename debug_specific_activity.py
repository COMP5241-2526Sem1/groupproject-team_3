"""
检查特定活动的数据结构
"""
from services.db_service import db_service
import json

# Connect to database
db_service._connect()

# Find the "Object-oriented programming" activity
activity = db_service._db.activities.find_one({
    'title': {'$regex': 'Object-oriented programming', '$options': 'i'}
})

if not activity:
    print("❌ Activity not found!")
    print("\nSearching for all poll activities...")
    activities = list(db_service._db.activities.find({'type': 'poll'}).sort('created_at', -1).limit(3))
    for act in activities:
        print(f"- {act['title']} (link: {act.get('link', 'N/A')})")
else:
    print("=" * 80)
    print(f"活动标题: {activity['title']}")
    print(f"活动链接: /a/{activity.get('link', 'MISSING')}")
    print(f"活动类型: {activity['type']}")
    print(f"创建时间: {activity.get('created_at')}")
    print("=" * 80)
    
    content = activity.get('content', {})
    print(f"\n📋 Content 字段:")
    print(f"Keys: {list(content.keys())}")
    print()
    
    # Check questions field
    if 'questions' in content:
        print("✅ 有 'questions' 字段 (多问题格式)")
        questions = content['questions']
        print(f"类型: {type(questions)}")
        print(f"长度: {len(questions) if isinstance(questions, list) else 'N/A'}")
        
        if isinstance(questions, list) and len(questions) > 0:
            print(f"\n第一个问题:")
            print(json.dumps(questions[0], indent=2, ensure_ascii=False))
            
            print(f"\n所有问题标题:")
            for i, q in enumerate(questions, 1):
                print(f"  {i}. {q.get('question', 'NO QUESTION FIELD')[:80]}")
    else:
        print("❌ 没有 'questions' 字段")
    
    # Check question field (singular)
    if 'question' in content:
        print(f"\n✅ 有 'question' 字段 (单问题格式)")
        print(f"Question: {content['question'][:100]}")
    else:
        print(f"\n❌ 没有 'question' 字段")
    
    print("\n" + "=" * 80)
    print("完整的 content 结构:")
    print(json.dumps(content, indent=2, ensure_ascii=False))
