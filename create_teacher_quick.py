"""
Quick create teacher account - non-interactive version
Creates a new teacher account with predefined credentials
"""

from services.db_service import db_service
from services.auth_service import AuthService
from models.user import User
import sys

def create_teacher_account_auto():
    """Create a new teacher account with auto-generated credentials"""
    
    # Predefined teacher account details
    username = "teacher_test"
    email = "teacher_test@example.com"
    password = "Teacher123"
    institution = "Test University"
    
    print("="*60)
    print("  Creating New Teacher Test Account")
    print("="*60)
    print()
    
    # Check if username already exists
    existing_user = User.find_by_username(username)
    if existing_user:
        print(f"❌ Error: Username '{username}' already exists!")
        print(f"   Trying alternative username...")
        
        # Try with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        username = f"teacher_test_{timestamp}"
        
        existing_user = User.find_by_username(username)
        if existing_user:
            print(f"❌ Error: Even '{username}' exists!")
            return False
    
    # Check if email already exists
    existing_email = User.find_by_email(email)
    if existing_email:
        print(f"⚠️  Warning: Email '{email}' already exists, using alternative...")
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        email = f"teacher_test_{timestamp}@example.com"
    
    # Create new teacher using auth service
    try:
        auth_service = AuthService()
        
        result = auth_service.register_user(
            username=username,
            password=password,
            email=email,
            role='teacher',
            institution=institution
        )
        
        if result.get('success'):
            user_id = result.get('user_id')
            print("\n✅ Teacher account created successfully!")
            print(f"\n📋 Account Details:")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Role: teacher")
            print(f"   Institution: {institution}")
            print(f"   User ID: {user_id}")
            print(f"\n🔗 Login URL: http://localhost:5000/auth/login")
            print(f"\n💡 Use these credentials to test teacher features!")
            return True
        else:
            print(f"❌ Failed to create teacher account: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating teacher account: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_teacher_account_auto()
    
    if not success:
        sys.exit(1)
