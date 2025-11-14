"""
Migrate all existing UTC timestamps to Hong Kong timezone (UTC+8)
Run this script once to convert all old data
"""

from datetime import datetime, timezone, timedelta
from config import Config
from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection
client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Hong Kong timezone
HK_TZ = timezone(timedelta(hours=8))

def convert_utc_to_hk(dt):
    """
    Convert a naive UTC datetime to naive HK datetime (adds 8 hours)
    MongoDB stores datetime as naive, so we just add 8 hours
    """
    if dt is None:
        return None
    
    # If already timezone-aware, remove timezone info but keep the HK time
    if dt.tzinfo is not None:
        # Check if it's already HK time (UTC+8)
        offset_hours = dt.utcoffset().total_seconds() / 3600 if dt.utcoffset() else 0
        if offset_hours == 8:
            # Already HK time, just remove tzinfo
            return dt.replace(tzinfo=None)
        else:
            # Convert to HK and remove tzinfo
            hk_time = dt.astimezone(HK_TZ)
            return hk_time.replace(tzinfo=None)
    
    # If naive, assume it's UTC and add 8 hours to get HK time
    hk_time = dt + timedelta(hours=8)
    return hk_time

def migrate_collection(collection_name, timestamp_fields):
    """
    Migrate timestamp fields in a collection
    
    Args:
        collection_name: Name of the collection
        timestamp_fields: List of field names that contain timestamps
    """
    print(f"\n{'='*60}")
    print(f"Migrating collection: {collection_name}")
    print(f"{'='*60}")
    
    collection = db[collection_name]
    documents = list(collection.find({}))
    
    if not documents:
        print(f"No documents found in {collection_name}")
        return
    
    print(f"Found {len(documents)} documents")
    updated_count = 0
    
    for doc in documents:
        doc_id = doc['_id']
        update_fields = {}
        has_updates = False
        
        # Check each timestamp field
        for field in timestamp_fields:
            # Handle nested fields (e.g., 'responses.submitted_at')
            if '.' in field:
                # For nested arrays like responses
                parts = field.split('.')
                if parts[0] in doc and isinstance(doc[parts[0]], list):
                    # Update each item in the array
                    for i, item in enumerate(doc[parts[0]]):
                        if parts[1] in item:
                            old_dt = item[parts[1]]
                            new_dt = convert_utc_to_hk(old_dt)
                            if new_dt != old_dt:
                                update_fields[f'{parts[0]}.{i}.{parts[1]}'] = new_dt
                                has_updates = True
            else:
                # Simple field
                if field in doc:
                    old_dt = doc[field]
                    new_dt = convert_utc_to_hk(old_dt)
                    if new_dt != old_dt:
                        update_fields[field] = new_dt
                        has_updates = True
        
        # Update document if there are changes
        if has_updates:
            result = collection.update_one(
                {'_id': doc_id},
                {'$set': update_fields}
            )
            if result.modified_count > 0:
                updated_count += 1
                print(f"✓ Updated document {doc_id}")
    
    print(f"\nCompleted: {updated_count}/{len(documents)} documents updated")

def migrate_responses_separately():
    """
    Special handling for responses array in activities collection
    """
    print(f"\n{'='*60}")
    print(f"Migrating activity responses timestamps")
    print(f"{'='*60}")
    
    collection = db['activities']
    activities = list(collection.find({'responses': {'$exists': True, '$ne': []}}))
    
    if not activities:
        print("No activities with responses found")
        return
    
    print(f"Found {len(activities)} activities with responses")
    updated_count = 0
    
    for activity in activities:
        activity_id = activity['_id']
        responses = activity.get('responses', [])
        
        has_updates = False
        
        for i, response in enumerate(responses):
            # Update submitted_at
            if 'submitted_at' in response:
                old_dt = response['submitted_at']
                new_dt = convert_utc_to_hk(old_dt)
                if new_dt != old_dt:
                    collection.update_one(
                        {'_id': activity_id},
                        {'$set': {f'responses.{i}.submitted_at': new_dt}}
                    )
                    has_updates = True
            
            # Update feedback_at if exists
            if 'feedback_at' in response:
                old_dt = response['feedback_at']
                new_dt = convert_utc_to_hk(old_dt)
                if new_dt != old_dt:
                    collection.update_one(
                        {'_id': activity_id},
                        {'$set': {f'responses.{i}.feedback_at': new_dt}}
                    )
                    has_updates = True
        
        if has_updates:
            updated_count += 1
            print(f"✓ Updated activity {activity_id} responses")
    
    print(f"\nCompleted: {updated_count}/{len(activities)} activities updated")

def main():
    """Main migration function"""
    print("="*60)
    print("TIMESTAMP MIGRATION TO HONG KONG TIME (UTC+8)")
    print("="*60)
    print(f"Current HK time: {datetime.now(HK_TZ)}")
    print(f"Database: {Config.DATABASE_NAME}")
    
    # Migrate users collection
    migrate_collection('users', ['created_at', 'last_login'])
    
    # Migrate courses collection
    migrate_collection('courses', ['created_at', 'updated_at'])
    
    # Migrate activities collection (main fields)
    migrate_collection('activities', ['created_at', 'updated_at'])
    
    # Migrate activity responses (nested fields)
    migrate_responses_separately()
    
    # Migrate students collection
    migrate_collection('students', ['created_at', 'enrolled_at'])
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETED!")
    print("="*60)
    print("All timestamps have been converted to Hong Kong time (UTC+8)")
    print("You can now restart your Flask application")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
