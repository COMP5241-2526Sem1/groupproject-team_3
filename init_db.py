"""
Database Initialization Script
Creates initial admin account and sets up database collections
"""

from services.db_service import db_service
from services.auth_service import auth_service
from models.user import User
from models.course import Course
from models.activity import Activity
from models.student import Student
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """
    Initialize database with default data
    Creates admin account and ensures collections exist
    """
    logger.info("Starting database initialization...")
    
    try:
        # Check if admin already exists
        admin = User.find_by_username('admin')
        
        if not admin:
            # Create default admin account
            logger.info("Creating default admin account...")
            result = auth_service.register_user(
                username='admin',
                password='admin123',
                email='admin@system.com',
                role='admin',
                institution='System'
            )
            
            if result['success']:
                logger.info("✓ Default admin account created")
                logger.info("  Username: admin")
                logger.info("  Password: admin123")
                logger.info("  ⚠️  IMPORTANT: Change this password after first login!")
            else:
                logger.error(f"✗ Failed to create admin account: {result['message']}")
        else:
            logger.info("✓ Admin account already exists")
        
        # Verify collections exist
        collections = db_service.db.list_collection_names()
        logger.info(f"✓ Database collections: {', '.join(collections)}")
        
        # Display statistics
        stats = {
            'users': db_service.count_documents(User.COLLECTION_NAME),
            'courses': db_service.count_documents(Course.COLLECTION_NAME),
            'activities': db_service.count_documents(Activity.COLLECTION_NAME),
            'students': db_service.count_documents(Student.COLLECTION_NAME)
        }
        
        logger.info("\nDatabase Statistics:")
        logger.info(f"  Users: {stats['users']}")
        logger.info(f"  Courses: {stats['courses']}")
        logger.info(f"  Activities: {stats['activities']}")
        logger.info(f"  Students: {stats['students']}")
        
        logger.info("\n✓ Database initialization completed successfully!")
        logger.info("\nYou can now start the application with: python app.py")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        logger.error("\nPlease check:")
        logger.error("  1. MongoDB connection string in .env file")
        logger.error("  2. Network connectivity to MongoDB Cloud")
        logger.error("  3. MongoDB Atlas IP whitelist settings")
        return False

def create_sample_data():
    """
    Create sample data for testing (optional)
    Only run this in development environment
    """
    logger.info("\nCreating sample data...")
    
    try:
        # Create sample teacher
        teacher_result = auth_service.register_user(
            username='teacher_demo',
            password='demo123',
            email='teacher@demo.com',
            role='teacher',
            institution='Hong Kong University'
        )
        
        if teacher_result['success']:
            teacher_id = teacher_result['user_id']
            logger.info("✓ Sample teacher created (username: teacher_demo, password: demo123)")
            
            # Create sample course
            from models.course import Course
            course = Course(
                name='Introduction to Computer Science',
                code='CS101',
                teacher_id=teacher_id,
                description='Basic computer science concepts'
            )
            course_id = course.save()
            logger.info("✓ Sample course created")
            
            # Create sample students
            from models.student import Student
            sample_students = [
                Student('S001', 'Alice Wong', course_id, 'alice@student.edu'),
                Student('S002', 'Bob Chen', course_id, 'bob@student.edu'),
                Student('S003', 'Charlie Lee', course_id, 'charlie@student.edu')
            ]
            
            for student in sample_students:
                student.save()
            
            logger.info("✓ Sample students created")
            
            # Create sample activity
            from models.activity import Activity
            activity = Activity(
                title='Python Basics Quiz',
                activity_type=Activity.TYPE_POLL,
                content={
                    'question': 'What is Python?',
                    'options': [
                        'A programming language',
                        'A type of snake',
                        'A software tool',
                        'All of the above'
                    ],
                    'allow_multiple': False
                },
                course_id=course_id,
                teacher_id=teacher_id
            )
            activity_id = activity.save()
            logger.info("✓ Sample activity created")
            
            logger.info("\n✓ Sample data created successfully!")
        else:
            logger.info("Sample teacher already exists, skipping sample data creation")
        
    except Exception as e:
        logger.error(f"✗ Failed to create sample data: {e}")

if __name__ == '__main__':
    import sys
    
    # Initialize database
    success = init_database()
    
    if success:
        # Ask if user wants to create sample data
        if len(sys.argv) > 1 and sys.argv[1] == '--sample':
            create_sample_data()
    else:
        sys.exit(1)
