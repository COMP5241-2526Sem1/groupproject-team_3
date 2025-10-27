"""
Fix activity response field names in database
修复数据库中活动响应的字段名
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db_service import db_service
from bson import ObjectId

def fix_response_fields():
    """
    Fix misnamed fields in activity responses
    """
    print("=" * 70)
    print("🔧 Fixing Activity Response Field Names")
    print("=" * 70)
    print()
    
    activities_collection = db_service.get_collection('activities')
    
    # Fix short answer responses: 'answer' -> 'text'
    print("1️⃣ Fixing short_answer activities...")
    short_answer_activities = list(activities_collection.find({
        'type': 'short_answer',
        'responses.answer': {'$exists': True}
    }))
    
    fixed_short_answer = 0
    for activity in short_answer_activities:
        activity_id = activity['_id']
        responses = activity.get('responses', [])
        
        updated_responses = []
        for response in responses:
            if 'answer' in response and 'text' not in response:
                response['text'] = response.pop('answer')
            updated_responses.append(response)
        
        activities_collection.update_one(
            {'_id': activity_id},
            {'$set': {'responses': updated_responses}}
        )
        fixed_short_answer += 1
    
    print(f"   Updated {fixed_short_answer} short_answer activities")
    print()
    
    # Fix word cloud responses: 'words' -> 'keywords'
    print("2️⃣ Fixing word_cloud activities...")
    
    word_cloud_activities = list(activities_collection.find({
        'type': 'word_cloud',
        'responses.words': {'$exists': True}
    }))
    
    fixed_word_cloud = 0
    for activity in word_cloud_activities:
        activity_id = activity['_id']
        responses = activity.get('responses', [])
        
        updated_responses = []
        for response in responses:
            if 'words' in response and 'keywords' not in response:
                # Convert 'words' (string) to 'keywords' (array)
                words_string = response.pop('words')
                # Split by comma or space to create array
                keywords = [w.strip() for w in words_string.replace(',', ' ').split() if w.strip()]
                response['keywords'] = keywords
            updated_responses.append(response)
        
        activities_collection.update_one(
            {'_id': activity_id},
            {'$set': {'responses': updated_responses}}
        )
        fixed_word_cloud += 1
    
    print(f"   Updated {fixed_word_cloud} word_cloud activities")
    print()
    
    # Remove obsolete 'timestamp' field (we use 'submitted_at')
    print("3️⃣ Removing obsolete 'timestamp' field...")
    all_activities = list(activities_collection.find({
        'responses.timestamp': {'$exists': True}
    }))
    
    cleaned_count = 0
    for activity in all_activities:
        activity_id = activity['_id']
        responses = activity.get('responses', [])
        
        updated_responses = []
        for response in responses:
            if 'timestamp' in response:
                response.pop('timestamp')
            updated_responses.append(response)
        
        activities_collection.update_one(
            {'_id': activity_id},
            {'$set': {'responses': updated_responses}}
        )
        cleaned_count += 1
    
    print(f"   Cleaned up {cleaned_count} activities")
    print()
    
    print("=" * 70)
    print("✅ Fix completed!")
    print("=" * 70)
    print()
    print("Summary of changes:")
    print(f"- Short answer: 'answer' → 'text' ({fixed_short_answer} activities)")
    print(f"- Word cloud: 'words' → 'keywords' ({fixed_word_cloud} activities)")
    print(f"- Removed: obsolete 'timestamp' field ({cleaned_count} activities)")
    print()
    print("You can now view activities without errors!")
    print()

if __name__ == '__main__':
    try:
        print("⚠️  This will modify the database!")
        print("Make sure you have a backup if needed.")
        print()
        
        response = input("Continue? (yes/no): ").strip().lower()
        
        if response == 'yes':
            fix_response_fields()
            print("✅ Database fix completed successfully!")
        else:
            print("❌ Operation cancelled.")
    
    except Exception as e:
        print(f"❌ Error during fix: {e}")
        import traceback
        traceback.print_exc()
