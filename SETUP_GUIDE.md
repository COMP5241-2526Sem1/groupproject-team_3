# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- MongoDB Cloud account (MongoDB Atlas)
- OpenAI API key

## Step 1: Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- pymongo (MongoDB driver)
- python-dotenv (Environment variables)
- openai (OpenAI API client)
- werkzeug (WSGI utilities)
- bcrypt (Password hashing)
- pandas (CSV processing)

## Step 2: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

2. Edit `.env` file and fill in your credentials:

### MongoDB Cloud Setup:
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account or sign in
3. Create a new cluster (free tier M0)
4. Click "Connect" → "Connect your application"
5. Copy the connection string
6. Replace `<password>` with your database password
7. Replace `<cluster>` with your cluster name
8. Paste the full string in `.env` as `MONGODB_URI`

Example:
```
MONGODB_URI=mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/learning_activity_system?retryWrites=true&w=majority
```

### OpenAI API Setup:
1. Go to https://platform.openai.com/api-keys
2. Create an account or sign in
3. Generate a new API key
4. Copy the key (starts with 'sk-')
5. Paste in `.env` as `OPENAI_API_KEY`

Example:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Secret Key:
Generate a secure secret key:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and paste it in `.env` as `SECRET_KEY`

## Step 3: Initialize Database

Run the initialization script to create the default admin account and setup database:

```powershell
python init_db.py
```

This will:
- Create necessary database collections
- Create default admin account (username: admin, password: admin123)
- Set up database indexes

**Optional**: Create sample data for testing:
```powershell
python init_db.py --sample
```

## Step 4: Start the Application

Run the Flask application:

```powershell
python app.py
```

You should see:
```
Starting application on 0.0.0.0:5000 (Environment: development)
Access the application at: http://localhost:5000
```

## Step 5: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### Default Accounts:

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Access: http://localhost:5000/admin

**Sample Teacher Account** (if sample data was created):
- Username: `teacher_demo`
- Password: `demo123`

⚠️ **Important**: Change the default admin password after first login!

## Testing the Application

### 1. Test Teacher Flow:
1. Register a new teacher account at `/register`
2. Login with your teacher credentials
3. Create a course (provide name and code)
4. Import students (manual or CSV)
5. Create learning activities (manual or AI-assisted)
6. Copy activity link and open in incognito/another browser
7. Submit student responses
8. View results and AI grouping (for short answers)

### 2. Test Admin Dashboard:
1. Login as admin
2. View system statistics
3. Browse teacher accounts and activities

### 3. Test AI Features:
1. Create activity using "AI-Assisted" method
2. Enter topic like "TCP/IP protocol basics"
3. Review AI-generated activity
4. Edit if needed and publish
5. Collect student responses
6. Use "Group Answers with AI" for short answer activities

## Troubleshooting

### MongoDB Connection Error:
- Check your connection string in `.env`
- Verify your IP is whitelisted in MongoDB Atlas (Network Access)
- Test connection: `python -c "from services.db_service import db_service; print('Connected!')"`

### OpenAI API Error:
- Verify your API key is correct
- Check API usage limits at https://platform.openai.com/usage
- Ensure you have credits available

### Port Already in Use:
- Change the port in `.env`: `APP_PORT=5001`
- Or kill the process using port 5000:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Module Not Found Error:
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Database Initialization Fails:
- Check MongoDB connection
- Ensure database name is correct
- Try deleting and recreating the database in MongoDB Atlas

## Project Structure

```
groupproject-team_3/
├── app.py                  # Main application entry point
├── config.py              # Configuration management
├── init_db.py            # Database initialization
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create from .env.example)
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
│
├── models/              # Data models
│   ├── user.py         # User model
│   ├── course.py       # Course model
│   ├── student.py      # Student model
│   └── activity.py     # Activity model
│
├── services/            # Business logic services
│   ├── db_service.py   # Database service
│   ├── auth_service.py # Authentication service
│   └── genai_service.py # AI service (GPT-4)
│
├── routes/              # API routes/endpoints
│   ├── auth_routes.py  # Authentication routes
│   ├── course_routes.py # Course management
│   ├── activity_routes.py # Activity management
│   └── admin_routes.py # Admin dashboard
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   └── js/
│       └── main.js     # Frontend JavaScript
│
└── templates/           # HTML templates
    ├── base.html       # Base template
    ├── login.html      # Login page
    ├── register.html   # Registration page
    ├── dashboard.html  # Teacher dashboard
    ├── course_detail.html # Course details
    ├── create_course.html # Create course
    ├── create_activity.html # Create activity
    ├── activity_detail.html # Activity details
    ├── student_activity.html # Student view
    ├── admin.html      # Admin dashboard
    └── error.html      # Error pages
```

## CSV Format for Student Import

Create a CSV file with the following format:

```csv
student_id,name,email
S001,Alice Wong,alice@student.edu
S002,Bob Chen,bob@student.edu
S003,Charlie Lee,charlie@student.edu
```

## API Endpoints

### Authentication
- `POST /register` - Register new teacher
- `POST /login` - User login
- `GET /logout` - User logout

### Courses
- `GET /dashboard` - Teacher dashboard
- `POST /course/create` - Create course
- `GET /course/<course_id>` - Course details
- `POST /course/<course_id>/import-students` - Import students

### Activities
- `POST /activity/create` - Create activity
- `POST /activity/ai-generate` - Generate activity with AI
- `GET /activity/<activity_id>` - Activity details
- `POST /activity/<activity_id>/submit` - Submit response
- `POST /activity/<activity_id>/group-answers` - Group answers with AI
- `GET /a/<link>` - Student activity page (no auth)

### Admin
- `GET /admin` - Admin dashboard
- `GET /admin/stats` - System statistics

## Development Notes

### Code Organization:
- **Models**: Define data structures and database operations
- **Services**: Implement business logic and external integrations
- **Routes**: Handle HTTP requests and responses
- **Templates**: Render HTML pages with Jinja2
- **Static**: CSS and JavaScript for frontend

### Security Features:
- Password hashing with bcrypt
- Session-based authentication
- CSRF protection (Flask built-in)
- Input validation on all forms
- Environment variables for secrets

### AI Integration:
- GPT-4 for activity generation
- Semantic analysis for answer grouping
- Fallback mechanisms when API unavailable

### Responsive Design:
- Mobile-first approach
- Tested on PC (1920×1080) and mobile (iPhone 12)
- CSS Grid and Flexbox for layouts

## Support

For issues or questions:
1. Check this setup guide
2. Review error messages in terminal
3. Check MongoDB Atlas and OpenAI dashboard
4. Verify all environment variables are set correctly

## License

MIT License - See LICENSE file for details
