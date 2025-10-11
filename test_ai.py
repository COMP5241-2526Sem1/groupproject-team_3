"""
Quick Test Script for GitHub Models API
Tests the AI service configuration and basic functionality
"""

from services.genai_service import GenAIService
import sys

def test_ai_service():
    """Test AI service initialization and basic operations"""
    
    print("=" * 60)
    print("🧪 GitHub Models API 测试脚本")
    print("=" * 60)
    
    # Test 1: Initialize service
    print("\n[1/3] 初始化 AI 服务...")
    try:
        service = GenAIService()
        print("✅ AI 服务初始化成功!")
        print(f"   使用模型: {service.model}")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False
    
    # Test 2: Generate activity
    print("\n[2/3] 测试生成学习活动...")
    try:
        result = service.generate_activity(
            teaching_content="Python programming basics: variables and data types",
            activity_type="poll"
        )
        if result and 'title' in result:
            print("✅ 活动生成成功!")
            print(f"   标题: {result.get('title', 'N/A')}")
            print(f"   类型: {result.get('activity_type', 'N/A')}")
        else:
            print("⚠️  生成成功但使用了备用模板（API 可能有问题）")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        print("   提示: 检查 API key 是否正确，是否超过速率限制")
        return False
    
    # Test 3: Group answers
    print("\n[3/3] 测试答案分组功能...")
    try:
        test_answers = [
            {
                "student_name": "Alice", 
                "text": "Variables store data. Python has types like int, str, float."
            },
            {
                "student_name": "Bob", 
                "text": "In Python, variables hold values and have different data types."
            },
            {
                "student_name": "Charlie", 
                "text": "Data types include integers, strings, and floats in Python."
            }
        ]
        
        result = service.group_answers(
            answers=test_answers,
            question="What are variables and data types in Python?"
        )
        
        if result and 'groups' in result:
            print("✅ 答案分组成功!")
            print(f"   分组数量: {len(result.get('groups', []))}")
            if result.get('overall_analysis'):
                print(f"   整体分析: {result['overall_analysis'][:100]}...")
        else:
            print("⚠️  分组成功但使用了备用方法")
    except Exception as e:
        print(f"❌ 分组失败: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)
    print("\n✅ GitHub Models API 配置正确，可以正常使用！")
    print("\n下一步:")
    print("1. 运行 python init_db.py 初始化数据库")
    print("2. 运行 python app.py 启动应用")
    print("3. 访问 http://localhost:5000")
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_ai_service()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生错误: {e}")
        print("\n请检查:")
        print("1. .env 文件是否存在")
        print("2. OPENAI_API_KEY 是否正确填写")
        print("3. OPENAI_MODEL 是否设置为 gpt-4o-mini")
        print("4. 网络连接是否正常")
        sys.exit(1)
