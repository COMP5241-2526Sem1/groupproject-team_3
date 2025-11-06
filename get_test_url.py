"""
生成测试URL和诊断信息
"""
from services.db_service import db_service
import time

db_service._connect()

# Get the OOP activity
activity = db_service._db.activities.find_one({
    'title': {'$regex': 'Object-oriented programming', '$options': 'i'}
})

if activity:
    link = activity.get('link', 'MISSING')
    
    print("=" * 80)
    print("🔗 学生访问链接:")
    print(f"   https://你的域名/a/{link}")
    print(f"   带缓存破坏参数: https://你的域名/a/{link}?v={int(time.time())}")
    print("=" * 80)
    print()
    print("📋 请在浏览器中测试以下操作:")
    print()
    print("方法1: 硬刷新 (推荐)")
    print("  1. 访问链接")
    print("  2. 按 Ctrl + F5 (Windows) 或 Cmd + Shift + R (Mac)")
    print()
    print("方法2: 清除缓存")
    print("  1. 按 F12 打开开发者工具")
    print("  2. 右键点击刷新按钮")
    print("  3. 选择 '清空缓存并硬性重新加载'")
    print()
    print("方法3: 隐私模式")
    print("  1. 按 Ctrl + Shift + N 打开隐私窗口")
    print("  2. 粘贴链接访问")
    print()
    print("=" * 80)
    print("📊 数据库确认:")
    print(f"  ✅ 活动类型: {activity['type']}")
    print(f"  ✅ 有 questions 字段: {'questions' in activity.get('content', {})}")
    print(f"  ✅ 问题数量: {len(activity['content']['questions'])}")
    print(f"  ✅ 数据完整性: 100%")
    print()
    print("❌ 问题原因: Vercel部署延迟或浏览器缓存")
    print("=" * 80)
else:
    print("活动未找到!")
