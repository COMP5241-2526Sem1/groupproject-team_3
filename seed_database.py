"""
Seed Database with Test Data
Creates sample courses and activities for testing
"""

from services.db_service import db_service
from models.user import User
from models.course import Course
from models.activity import Activity
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """Populate database with test data"""
    
    logger.info("=" * 60)
    logger.info("🌱 Starting Database Seeding")
    logger.info("=" * 60)
    
    # Get test teacher
    teacher = User.find_by_username('teacher_demo')
    if not teacher:
        logger.error("❌ Teacher account 'teacher_demo' not found!")
        logger.info("Please run: python create_test_accounts.py first")
        return
    
    teacher_id = str(teacher['_id'])
    logger.info(f"✓ Found teacher: {teacher['username']} (ID: {teacher_id})")
    
    # Create sample courses
    courses_data = [
        {
            'name': 'Introduction to Python Programming',
            'code': 'CS101',
            'description': 'Learn the fundamentals of Python programming including variables, loops, functions, and object-oriented programming.',
            'teacher_id': teacher_id
        },
        {
            'name': 'Data Structures and Algorithms',
            'code': 'CS102',
            'description': 'Master essential data structures (arrays, linked lists, trees, graphs) and algorithms (sorting, searching, dynamic programming).',
            'teacher_id': teacher_id
        },
        {
            'name': 'Web Development with Flask',
            'code': 'CS201',
            'description': 'Build modern web applications using Flask framework, HTML, CSS, JavaScript, and databases.',
            'teacher_id': teacher_id
        },
        {
            'name': 'Machine Learning Fundamentals',
            'code': 'CS301',
            'description': 'Introduction to machine learning concepts, supervised and unsupervised learning, neural networks, and practical applications.',
            'teacher_id': teacher_id
        },
        {
            'name': 'Database Management Systems',
            'code': 'CS202',
            'description': 'Learn SQL, database design, normalization, transactions, and work with MongoDB and PostgreSQL.',
            'teacher_id': teacher_id
        }
    ]
    
    created_courses = []
    
    logger.info("\n📚 Creating Courses...")
    logger.info("-" * 60)
    
    for course_data in courses_data:
        # Check if course already exists
        existing = Course.find_by_code(course_data['code'])
        if existing:
            logger.info(f"⚠️  Course {course_data['code']} already exists - skipped")
            created_courses.append(existing)
            continue
        
        course = Course(
            name=course_data['name'],
            code=course_data['code'],
            teacher_id=course_data['teacher_id'],
            description=course_data['description']
        )
        course.save()
        created_courses.append(Course.find_by_code(course_data['code']))
        logger.info(f"✅ Created: {course_data['code']} - {course_data['name']}")
    
    # Create sample activities for each course
    logger.info("\n📝 Creating Activities...")
    logger.info("-" * 60)
    
    activities_templates = {
        'CS101': [
            {
                'title': 'Python Basics Quiz',
                'type': 'poll',
                'content': {
                    'question': 'Which of the following is the correct way to declare a variable in Python?',
                    'options': [
                        'var x = 10',
                        'int x = 10',
                        'x = 10',
                        'declare x = 10'
                    ],
                    'ai_generated': False
                }
            },
            {
                'title': 'What is your favorite Python feature?',
                'type': 'word_cloud',
                'content': {
                    'prompt': 'Share your favorite Python feature or concept in one or two words',
                    'max_words': 3,
                    'ai_generated': False
                }
            },
            {
                'title': 'Explain List Comprehension',
                'type': 'short_answer',
                'content': {
                    'question': 'Explain what list comprehension is in Python and provide an example.',
                    'word_limit': 150,
                    'ai_generated': False
                }
            }
        ],
        'CS102': [
            {
                'title': 'Time Complexity Poll',
                'type': 'poll',
                'content': {
                    'question': 'What is the time complexity of binary search?',
                    'options': [
                        'O(n)',
                        'O(log n)',
                        'O(n²)',
                        'O(1)'
                    ],
                    'ai_generated': False
                }
            },
            {
                'title': 'Sorting Algorithm Experience',
                'type': 'short_answer',
                'content': {
                    'question': 'Which sorting algorithm do you find most interesting and why?',
                    'word_limit': 200,
                    'ai_generated': False
                }
            },
            {
                'title': 'Data Structure Keywords',
                'type': 'word_cloud',
                'content': {
                    'prompt': 'What comes to mind when you think of data structures?',
                    'max_words': 2,
                    'ai_generated': False
                }
            }
        ],
        'CS201': [
            {
                'title': 'HTTP Methods Quiz',
                'type': 'poll',
                'content': {
                    'question': 'Which HTTP method is used to create a new resource?',
                    'options': [
                        'GET',
                        'POST',
                        'PUT',
                        'DELETE'
                    ],
                    'ai_generated': False
                }
            },
            {
                'title': 'Flask vs Django',
                'type': 'short_answer',
                'content': {
                    'question': 'Compare Flask and Django frameworks. What are the main differences?',
                    'word_limit': 200,
                    'ai_generated': False
                }
            }
        ],
        'CS301': [
            {
                'title': 'ML Algorithm Type',
                'type': 'poll',
                'content': {
                    'question': 'Is linear regression a supervised or unsupervised learning algorithm?',
                    'options': [
                        'Supervised',
                        'Unsupervised',
                        'Both',
                        'Neither'
                    ],
                    'ai_generated': False
                }
            },
            {
                'title': 'Neural Network Concepts',
                'type': 'word_cloud',
                'content': {
                    'prompt': 'What neural network concept interests you most?',
                    'max_words': 3,
                    'ai_generated': False
                }
            },
            {
                'title': 'Overfitting Explanation',
                'type': 'short_answer',
                'content': {
                    'question': 'Explain what overfitting is in machine learning and how to prevent it.',
                    'word_limit': 180,
                    'ai_generated': False
                }
            }
        ],
        'CS202': [
            {
                'title': 'SQL vs NoSQL',
                'type': 'poll',
                'content': {
                    'question': 'Which database type is better for handling unstructured data?',
                    'options': [
                        'SQL (Relational)',
                        'NoSQL (Document)',
                        'Both are equal',
                        'Neither'
                    ],
                    'ai_generated': False
                }
            },
            {
                'title': 'Database Normalization',
                'type': 'short_answer',
                'content': {
                    'question': 'Explain the concept of database normalization and its benefits.',
                    'word_limit': 150,
                    'ai_generated': False
                }
            }
        ]
    }
    
    total_activities = 0
    
    for course in created_courses:
        course_code = course['code']
        course_id = str(course['_id'])
        
        if course_code in activities_templates:
            activities = activities_templates[course_code]
            
            for activity_data in activities:
                # Check if activity already exists
                existing_activities = Activity.find_by_course(course_id)
                if any(a['title'] == activity_data['title'] for a in existing_activities):
                    logger.info(f"⚠️  Activity '{activity_data['title']}' already exists - skipped")
                    continue
                
                activity = Activity(
                    title=activity_data['title'],
                    activity_type=activity_data['type'],
                    content=activity_data['content'],
                    course_id=course_id,
                    teacher_id=teacher_id
                )
                activity.save()
                total_activities += 1
                
                type_icon = {'poll': '📊', 'short_answer': '✍️', 'word_cloud': '☁️'}.get(activity_data['type'], '📝')
                logger.info(f"  ✅ {type_icon} {activity_data['title']}")
    
    # Add some sample responses from students
    logger.info("\n👥 Adding Sample Student Responses...")
    logger.info("-" * 60)
    
    students = [
        User.find_by_username('student_demo'),
        User.find_by_username('alice_wang'),
        User.find_by_username('bob_chen')
    ]
    
    # Filter out None values
    students = [s for s in students if s is not None]
    
    if not students:
        logger.warning("⚠️  No student accounts found. Responses not added.")
    else:
        # Enroll students in courses
        for student in students:
            student_obj = User.find_by_id(str(student['_id']))
            if student_obj:
                for course in created_courses[:3]:  # Enroll in first 3 courses
                    course_id = str(course['_id'])
                    if course_id not in student_obj.get('enrolled_courses', []):
                        User.enroll_course(str(student['_id']), course_id)
                        logger.info(f"  📚 Enrolled {student['username']} in {course['code']}")
        
        # Add sample responses to some activities
        sample_responses = 0
        for course in created_courses[:2]:  # First 2 courses
            activities = list(Activity.find_by_course(str(course['_id'])))
            
            for activity in activities[:2]:  # First 2 activities per course
                for student in students[:2]:  # First 2 students
                    response_data = None
                    
                    if activity['type'] == 'poll':
                        response_data = {
                            'student_id': student.get('student_id', 'Unknown'),
                            'student_name': student['username'],
                            'answer': activity['content']['options'][0],
                            'timestamp': datetime.utcnow()
                        }
                    elif activity['type'] == 'word_cloud':
                        response_data = {
                            'student_id': student.get('student_id', 'Unknown'),
                            'student_name': student['username'],
                            'words': 'Learning Python Programming',
                            'timestamp': datetime.utcnow()
                        }
                    elif activity['type'] == 'short_answer':
                        response_data = {
                            'student_id': student.get('student_id', 'Unknown'),
                            'student_name': student['username'],
                            'answer': 'This is a sample answer to demonstrate the activity functionality.',
                            'timestamp': datetime.utcnow()
                        }
                    
                    if response_data:
                        Activity.add_response(str(activity['_id']), response_data)
                        sample_responses += 1
        
        logger.info(f"  ✅ Added {sample_responses} sample responses")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("✨ Database Seeding Completed!")
    logger.info("=" * 60)
    logger.info(f"📚 Courses created: {len(created_courses)}")
    logger.info(f"📝 Activities created: {total_activities}")
    logger.info(f"👥 Students enrolled: {len(students)}")
    logger.info("\n🎯 You can now test the system with rich data!")
    logger.info("=" * 60)

if __name__ == '__main__':
    try:
        seed_database()
    except Exception as e:
        logger.error(f"❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
