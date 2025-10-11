# Interactive Learning Activity Management System

A comprehensive learning activity management platform for university lecturers in Hong Kong, featuring AI-powered activity generation and student response analysis.

## Features

- **User Management**: Teacher registration/login with encrypted passwords, admin dashboard
- **Course Management**: Create courses, import student information (manual/CSV)
- **Learning Activities**: Create polls, short-answer questions, and word clouds
- **AI Integration**: GPT-4 powered activity generation and automatic answer grouping
- **Responsive Design**: Works on PC (1920×1080) and mobile devices (iPhone 12)

## Technology Stack

- **Backend**: Python 3.8+, Flask
- **Database**: MongoDB Cloud
- **AI**: OpenAI GPT-4.1-MINI
- **Frontend**: HTML, CSS, JavaScript (Responsive Design)

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd groupproject-team_3
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your MongoDB Cloud connection string
   - Add your OpenAI API key
   - Generate a secure SECRET_KEY

```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Initialize the database**
```bash
python init_db.py
```

This will create:
- Default admin account (username: admin, password: admin123)
- Required database collections and indexes

## Running the Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Login with teacher account or admin account

## Usage Guide

### For Teachers

1. **Register/Login**
   - Navigate to `/register` to create a new teacher account
   - Login at `/login`

2. **Create Course**
   - Go to Dashboard → "Create New Course"
   - Enter course name and course code

3. **Import Students**
   - Select a course → "Import Students"
   - Option 1: Manual input (Student ID + Name)
   - Option 2: Upload CSV file (format: student_id,name)

4. **Create Learning Activity**
   - Manual Creation: Select activity type (Poll/Short Answer/Word Cloud)
   - AI-Assisted: Input teaching content or keywords, AI generates activity draft

5. **View Activity Results**
   - Click on activity to view participation stats
   - For short-answer questions, view AI-grouped responses

### For Administrators

1. **Login**
   - Default credentials: username `admin`, password `admin123`
   - Access admin dashboard at `/admin`

2. **View Statistics**
   - Total number of teachers
   - Total number of learning activities
   - System overview

## Project Structure

```
groupproject-team_3/
├── app.py                  # Main Flask application entry point
├── config.py              # Configuration management
├── init_db.py            # Database initialization script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── models/
│   ├── user.py           # User model (Teacher/Admin)
│   ├── course.py         # Course model
│   ├── activity.py       # Learning activity model
│   └── student.py        # Student model
├── services/
│   ├── auth_service.py   # Authentication service
│   ├── genai_service.py  # AI integration service (GPT-4)
│   └── db_service.py     # Database service
├── routes/
│   ├── auth_routes.py    # Authentication routes
│   ├── course_routes.py  # Course management routes
│   ├── activity_routes.py # Activity management routes
│   └── admin_routes.py   # Admin dashboard routes
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet (responsive)
│   └── js/
│       └── main.js       # Frontend JavaScript
└── templates/
    ├── base.html         # Base template
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # Teacher dashboard
    ├── admin.html        # Admin dashboard
    ├── course_detail.html # Course detail page
    ├── create_activity.html # Activity creation page
    ├── activity_detail.html # Activity detail page
    └── student_activity.html # Student participation page
```

## API Endpoints

### Authentication
- `POST /register` - Teacher registration
- `POST /login` - User login
- `GET /logout` - User logout

### Courses
- `GET /dashboard` - Teacher dashboard
- `POST /course/create` - Create new course
- `GET /course/<course_id>` - Course details
- `POST /course/<course_id>/import-students` - Import students

### Activities
- `POST /activity/create` - Create activity manually
- `POST /activity/ai-generate` - AI-assisted activity generation
- `GET /activity/<activity_id>` - Activity details
- `POST /activity/<activity_id>/submit` - Submit student response
- `POST /activity/<activity_id>/group-answers` - AI answer grouping

### Admin
- `GET /admin` - Admin dashboard
- `GET /admin/stats` - System statistics

## Database Collections

### users
- Stores teacher and admin accounts
- Fields: username, password (hashed), role, email, institution

### courses
- Stores course information
- Fields: name, code, teacher_id, students, created_at

### activities
- Stores learning activities
- Fields: type, title, content, course_id, teacher_id, responses, link

### students
- Stores student information
- Fields: student_id, name, course_id

## AI Features

### Activity Generation
- Input: Teaching content or keywords
- Output: 3 activity suggestions with questions and reference answers
- Editable before publishing

### Answer Grouping
- Analyzes student responses semantically
- Groups similar answers automatically
- Provides group summaries and insights

## Security Considerations

- Passwords are hashed using bcrypt
- Session management with Flask sessions
- Environment variables for sensitive data
- Input validation on all forms

## Testing

1. **Test Teacher Flow**
   - Register → Login → Create Course → Import Students → Create Activity

2. **Test Student Participation**
   - Access activity link (no login required)
   - Submit response

3. **Test AI Features**
   - Generate activity with AI
   - Submit multiple responses and test grouping

4. **Test Admin Dashboard**
   - Login as admin
   - View statistics

## Troubleshooting

### MongoDB Connection Issues
- Verify connection string in `.env`
- Check IP whitelist in MongoDB Atlas
- Ensure network connectivity

### OpenAI API Issues
- Verify API key is valid
- Check API rate limits
- Review error logs in console

### Port Already in Use
```bash
# Change port in .env or use different port
APP_PORT=5001
```

## Future Enhancements

- Real-time activity updates using WebSocket
- Advanced analytics and reporting
- Multi-language support with AI translation
- Mobile app development
- Integration with LMS platforms

## License

MIT License

## Contact

For questions or support, please contact the development team.
