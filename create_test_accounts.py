"""
Create Test Accounts Script
Creates teacher and student test accounts for system testing
"""

from services.db_service import db_service
from services.auth_service import auth_service
from models.user import User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_accounts():
    """
    Create test accounts for teachers and students
    """
    logger.info("=" * 60)
    logger.info("Creating Test Accounts")
    logger.info("=" * 60)
    
    test_accounts = []
    
    # Teacher Test Accounts
    teachers = [
        {
            'username': 'teacher_demo',
            'password': 'teacher123',
            'email': 'teacher.demo@university.edu',
            'role': 'teacher',
            'institution': 'Computer Science Department'
        },
        {
            'username': 'prof_smith',
            'password': 'prof123',
            'email': 'smith@university.edu',
            'role': 'teacher',
            'institution': 'Engineering Department'
        }
    ]
    
    # Student Test Accounts
    students = [
        {
            'username': 'student_demo',
            'password': 'student123',
            'email': 'student.demo@university.edu',
            'role': 'student',
            'institution': 'Computer Science',
            'student_id': 'S2024001'
        },
        {
            'username': 'alice_wang',
            'password': 'alice123',
            'email': 'alice.wang@university.edu',
            'role': 'student',
            'institution': 'Computer Science',
            'student_id': 'S2024002'
        },
        {
            'username': 'bob_chen',
            'password': 'bob123',
            'email': 'bob.chen@university.edu',
            'role': 'student',
            'institution': 'Engineering',
            'student_id': 'S2024003'
        }
    ]
    
    logger.info("\n📚 Creating Teacher Accounts...")
    logger.info("-" * 60)
    
    for teacher_data in teachers:
        # Check if user already exists
        existing_user = User.find_by_username(teacher_data['username'])
        
        if existing_user:
            logger.info(f"⚠️  Teacher '{teacher_data['username']}' already exists - skipped")
        else:
            result = auth_service.register_user(
                username=teacher_data['username'],
                password=teacher_data['password'],
                email=teacher_data['email'],
                role=teacher_data['role'],
                institution=teacher_data['institution']
            )
            
            if result['success']:
                logger.info(f"✅ Teacher account created successfully:")
                logger.info(f"   Username: {teacher_data['username']}")
                logger.info(f"   Password: {teacher_data['password']}")
                logger.info(f"   Email: {teacher_data['email']}")
                logger.info(f"   Institution: {teacher_data['institution']}")
                test_accounts.append({
                    'role': 'Teacher',
                    'username': teacher_data['username'],
                    'password': teacher_data['password']
                })
            else:
                logger.error(f"❌ Failed to create teacher '{teacher_data['username']}': {result['message']}")
        
        logger.info("")
    
    logger.info("\n👨‍🎓 Creating Student Accounts...")
    logger.info("-" * 60)
    
    for student_data in students:
        # Check if user already exists
        existing_user = User.find_by_username(student_data['username'])
        
        if existing_user:
            logger.info(f"⚠️  Student '{student_data['username']}' already exists - skipped")
        else:
            result = auth_service.register_user(
                username=student_data['username'],
                password=student_data['password'],
                email=student_data['email'],
                role=student_data['role'],
                institution=student_data['institution'],
                student_id=student_data['student_id']
            )
            
            if result['success']:
                logger.info(f"✅ Student account created successfully:")
                logger.info(f"   Username: {student_data['username']}")
                logger.info(f"   Password: {student_data['password']}")
                logger.info(f"   Email: {student_data['email']}")
                logger.info(f"   Student ID: {student_data['student_id']}")
                logger.info(f"   Institution: {student_data['institution']}")
                test_accounts.append({
                    'role': 'Student',
                    'username': student_data['username'],
                    'password': student_data['password'],
                    'student_id': student_data['student_id']
                })
            else:
                logger.error(f"❌ Failed to create student '{student_data['username']}': {result['message']}")
        
        logger.info("")
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST ACCOUNTS SUMMARY")
    logger.info("=" * 60)
    
    if test_accounts:
        logger.info("\n📋 Created Test Accounts:\n")
        
        teachers_list = [acc for acc in test_accounts if acc['role'] == 'Teacher']
        students_list = [acc for acc in test_accounts if acc['role'] == 'Student']
        
        if teachers_list:
            logger.info("👨‍🏫 TEACHER ACCOUNTS:")
            for acc in teachers_list:
                logger.info(f"   • Username: {acc['username']}")
                logger.info(f"     Password: {acc['password']}")
                logger.info("")
        
        if students_list:
            logger.info("👨‍🎓 STUDENT ACCOUNTS:")
            for acc in students_list:
                logger.info(f"   • Username: {acc['username']}")
                logger.info(f"     Password: {acc['password']}")
                logger.info(f"     Student ID: {acc['student_id']}")
                logger.info("")
        
        logger.info("\n🌐 Access the system at: http://localhost:5000")
        logger.info("📝 Login URL: http://localhost:5000/login")
        logger.info("")
    else:
        logger.info("ℹ️  All test accounts already exist in the database.")
    
    logger.info("=" * 60)
    logger.info("✨ Test account creation completed!")
    logger.info("=" * 60)

if __name__ == '__main__':
    try:
        create_test_accounts()
    except Exception as e:
        logger.error(f"❌ Error during test account creation: {str(e)}")
        import traceback
        traceback.print_exc()
