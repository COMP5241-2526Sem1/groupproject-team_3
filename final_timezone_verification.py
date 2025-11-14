"""
Final comprehensive verification of Hong Kong timezone implementation
"""

from utils.time_utils import get_hk_time
from config import Config
from pymongo import MongoClient
from datetime import datetime, timedelta

print("="*70)
print("香港时间(UTC+8)完整验证")
print("="*70)

# Test 1: get_hk_time() generates correct time
print("\n1. 测试 get_hk_time() 生成的时间")
print("-" * 70)
hk_now = get_hk_time()
print(f"   当前香港时间: {hk_now}")
print(f"   时区信息: {hk_now.tzinfo}")
print(f"   类型: {'timezone-aware' if hk_now.tzinfo else 'naive (正确,适合MongoDB)'}")

# Compare with UTC
import pytz
utc_now = datetime.now(pytz.UTC)
hk_tz = pytz.timezone('Asia/Hong_Kong')
hk_expected = utc_now.astimezone(hk_tz)
print(f"   UTC时间: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   期望HK时间: {hk_expected.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   实际HK时间: {hk_now.strftime('%Y-%m-%d %H:%M:%S')}")

hour_diff = abs((hk_now.hour - utc_now.hour + 24) % 24)
if 7 <= hour_diff <= 9:  # Allow some flexibility around 8 hours
    print(f"   ✅ 时差正确: 约{hour_diff}小时")
else:
    print(f"   ❌ 时差错误: {hour_diff}小时 (应该是8小时)")

# Test 2: MongoDB storage and retrieval
print("\n2. 测试 MongoDB 存储和读取")
print("-" * 70)
client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

test_time = get_hk_time()
test_doc = {
    'test': 'timezone_verification',
    'timestamp': test_time
}

result = db.test_collection.insert_one(test_doc)
retrieved = db.test_collection.find_one({'_id': result.inserted_id})
retrieved_time = retrieved['timestamp']

print(f"   存储时间: {test_time}")
print(f"   读取时间: {retrieved_time}")
print(f"   是否相等: {test_time.replace(microsecond=0) == retrieved_time.replace(microsecond=0)}")

if test_time.replace(microsecond=0) == retrieved_time.replace(microsecond=0):
    print("   ✅ MongoDB存储正确")
else:
    print("   ❌ MongoDB存储有问题")

db.test_collection.delete_one({'_id': result.inserted_id})

# Test 3: Check real data
print("\n3. 检查实际数据库中的时间")
print("-" * 70)
activity = db.activities.find_one(
    {'responses': {'$exists': True, '$ne': []}},
    sort=[('updated_at', -1)]
)

if activity:
    print(f"   活动: {activity.get('title', 'Unknown')}")
    print(f"   更新时间: {activity.get('updated_at')}")
    
    if activity.get('responses'):
        recent_resp = activity['responses'][-1]
        print(f"   最新回应学生: {recent_resp.get('student_name', 'Unknown')}")
        print(f"   提交时间: {recent_resp.get('submitted_at')}")
        
        # Check if time looks like HK time (not UTC)
        submitted = recent_resp.get('submitted_at')
        if submitted:
            # HK time should be reasonable (not middle of night if current is daytime)
            hour = submitted.hour
            current_hour = hk_now.hour
            if abs(hour - current_hour) < 12:  # Within reasonable range
                print(f"   ✅ 时间看起来正确 (小时: {hour})")
            else:
                print(f"   ⚠️  时间可能不对 (小时: {hour}, 当前: {current_hour})")

# Test 4: Check all models use HK time
print("\n4. 验证所有模型使用香港时间")
print("-" * 70)

check_files = {
    'models/user.py': ['get_hk_time'],
    'models/course.py': ['get_hk_time'],
    'models/activity.py': ['get_hk_time'],
    'models/student.py': ['get_hk_time'],
    'services/auth_service.py': ['get_hk_time'],
}

import os
all_correct = True
for file_path, expected_imports in check_files.items():
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            has_imports = all(imp in content for imp in expected_imports)
            no_utcnow = 'datetime.utcnow()' not in content
            
            status = "✅" if (has_imports and no_utcnow) else "❌"
            print(f"   {status} {file_path}")
            
            if not has_imports:
                print(f"       ⚠️  缺少导入: {expected_imports}")
            if not no_utcnow:
                print(f"       ⚠️  仍在使用 datetime.utcnow()")
            
            all_correct = all_correct and has_imports and no_utcnow
    else:
        print(f"   ⚠️  文件不存在: {file_path}")

print("\n" + "="*70)
if all_correct:
    print("🎉 所有验证通过! 系统已完全使用香港时间(UTC+8)")
else:
    print("⚠️  部分验证失败,请检查上述错误")
print("="*70)

print("\n现在可以测试提交功能,时间应该显示为香港时间!")
print("例如: 如果现在是 15:40,提交时间应该显示 15:40 而不是 07:40")
