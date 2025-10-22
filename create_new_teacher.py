"""
Create a new teacher test account
Quick script to add additional teacher accounts for testing
"""

from services.db_service import db_service
from models.user import User
import sys

def create_teacher_account():
    """Create a new teacher account"""
    
    # Teacher account details
    username = input("Enter username for new teacher (default: teacher_new): ").strip() or "teacher_new"
    email = input("Enter email (default: teacher_new@test.com): ").strip() or "teacher_new@test.com"
    password = input("Enter password (default: teacher123): ").strip() or "teacher123"
    institution = input("Enter institution (default: Test University): ").strip() or "Test University"
    
    # Check if username already exists
    existing_user = User.find_by_username(username)
    if existing_user:
        print(f"❌ Error: Username '{username}' already exists!")
        print(f"   Try another username or delete the existing user first.")
        return False
    
    # Check if email already exists
    existing_email = User.find_by_email(email)
    if existing_email:
        print(f"❌ Error: Email '{email}' already exists!")
        print(f"   Try another email or delete the existing user first.")
        return False
    
    # Create new teacher
    try:
        teacher = User(
            username=username,
            email=email,
            role='teacher',
            institution=institution,
            password=password
        )
        
        user_id = teacher.save()
        
        if user_id:
            print("\n✅ Teacher account created successfully!")
            print(f"\n📋 Account Details:")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Role: teacher")
            print(f"   Institution: {institution}")
            print(f"   User ID: {user_id}")
            print(f"\n🔗 Login at: http://localhost:5000/auth/login")
            return True
        else:
            print("❌ Failed to create teacher account")
            return False
            
    except Exception as e:
        print(f"❌ Error creating teacher account: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("  Create New Teacher Test Account")
    print("="*60)
    print()
    
    success = create_teacher_account()
    
    if not success:
        sys.exit(1)
