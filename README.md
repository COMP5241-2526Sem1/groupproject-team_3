# Interactive Learning Activity Management System

A comprehensive learning activity management platform for university lecturers in Hong Kong, featuring AI-powered activity generation and student response analysis.

## 🚀 Quick Start | 快速开始

**New users? Start here! | 新用户从这里开始！**

### 30-Second Setup | 30秒快速安装
👉 **[QUICK_START_30SEC.md](QUICK_START_30SEC.md)** - Get running in 30 seconds | 30秒快速启动

### Complete Guide | 完整指南
📘 **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Detailed installation guide (中英对照) | 详细安装指南

### MongoDB Setup | MongoDB 配置
🗄️ **[MONGODB_SETUP_GUIDE.md](MONGODB_SETUP_GUIDE.md)** - MongoDB Atlas configuration | MongoDB Atlas 配置指南

---

## 📚 Documentation | 文档索引

### For Users | 用户文档
- 🚀 **[Quick Start - 30 Seconds](QUICK_START_30SEC.md)** - Fastest way to get started
- 📖 **[Complete Setup Guide](QUICK_START_GUIDE.md)** - Step-by-step installation
- 🗄️ **[MongoDB Setup](MONGODB_SETUP_GUIDE.md)** - Database configuration
- 🧪 **[Testing Guide](TESTING_COMPLETE_GUIDE.md)** - How to test features

### For Developers | 开发者文档
- 🎨 **[Student Interface Design](STUDENT_INTERFACE_FINAL.md)** - UI/UX documentation
- 🐛 **[Bug Fix Records](DASHBOARD_COURSE_DETAIL_FIX.md)** - Error fixes log
- ⏰ **[Timestamp Fix Guide](TIMESTAMP_FIX_GUIDE.md)** - Timestamp display fix ⭐ NEW
- 📋 **[System Enhancement Plan](SYSTEM_ENHANCEMENT_PLAN.md)** - Roadmap
- 🔧 **[Project Delivery Guide](PROJECT_DELIVERY.md)** - Deployment guide

---

## ✨ Features | 功能特点

### 👨‍🎓 Student Interface | 学生界面
- ✅ **Dashboard** - Learning statistics and progress tracking | 学习统计和进度跟踪
- ✅ **My Courses** - Enrolled course management | 已选课程管理
- ✅ **Browse Courses** - Discover and enroll in courses | 浏览和选课
- ✅ **Course Details** - View activities and materials | 查看活动和资料
- ✅ **Activities** - Participate in polls, quizzes, word clouds | 参与投票、测验、词云
- ✅ **Submission Tracking** - View submission timestamps | 查看提交时间戳 ⭐
- 🔄 **Leaderboard** - Gamification (coming soon) | 排行榜（即将推出）

### 👨‍🏫 Teacher Interface | 教师界面
- ✅ **Course Management** - Create and manage courses | 创建和管理课程
- ✅ **Activity Creation** - Polls, short answers, word clouds | 投票、简答、词云
- ✅ **AI Generation** - GPT-4 powered content creation | GPT-4 驱动的内容生成
- ✅ **Student Management** - View enrolled students | 查看选课学生
- ✅ **Response Analysis** - View and analyze submissions | 查看和分析回答

### 🔐 Admin Interface | 管理员界面
- ✅ **User Management** - Manage all users | 管理所有用户
- ✅ **System Overview** - Platform statistics | 平台统计

---

## 🛠️ Technology Stack | 技术栈

- **Backend | 后端**: Python 3.8+, Flask 3.0.0
- **Database | 数据库**: MongoDB Atlas (Cloud)
- **AI | 人工智能**: OpenAI GPT-4 / GitHub Models
- **Frontend | 前端**: HTML5, CSS3, Jinja2 Templates
- **Authentication | 认证**: bcrypt password hashing

---

## 📦 Installation | 安装

### Quick Method | 快速方法

```bash
# 1. Clone repository | 克隆仓库
git clone https://github.com/COMP5241-2526Sem1/groupproject-team_3.git
cd groupproject-team_3
git checkout ZmhPre

# 2. Create virtual environment | 创建虚拟环境
python -m venv Project3
.\Project3\Scripts\Activate.ps1  # Windows
source Project3/bin/activate      # Mac/Linux

# 3. Install dependencies | 安装依赖
pip install -r requirements.txt

# 4. Configure .env | 配置环境变量
# Create .env file and add your MongoDB URI
# 创建 .env 文件并添加 MongoDB URI

# 5. Initialize database | 初始化数据库
python init_db.py
python seed_database.py

# 6. Run application | 运行应用
python app.py
```

### Detailed Instructions | 详细说明
See **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** for complete installation guide.

---

## 🔑 Test Accounts | 测试账号

### Student | 学生
```
Username: student_demo
Password: student123
```

### Teacher | 教师
```
Username: teacher_demo
Password: teacher123
```

### Admin | 管理员
```
Username: admin
Password: admin123
```

---

## 📱 Usage | 使用方法

### Start Application | 启动应用
```bash
# Activate virtual environment | 激活虚拟环境
.\Project3\Scripts\Activate.ps1  # Windows
source Project3/bin/activate      # Mac/Linux

# Run application | 运行应用
python app.py
```

### Access | 访问
Open browser and visit | 打开浏览器访问:
```
http://localhost:5000
```
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

### Timestamp Not Showing ⭐ (Fixed in v1.1)
**Issue**: Student submission timestamps showing blank  
**Solution**: See [TIMESTAMP_FIX_GUIDE.md](TIMESTAMP_FIX_GUIDE.md)  
**Status**: ✅ Fixed (2025-10-12)

---

## 🆕 Recent Updates | 最近更新

### v1.1 (2025-10-12)
- ✅ Fixed timestamp display issue in activity submissions
- ✅ Added comprehensive documentation (TIMESTAMP_FIX_GUIDE.md)
- ✅ Updated DASHBOARD_COURSE_DETAIL_FIX.md with timestamp fix
- ✅ Updated TESTING_COMPLETE_GUIDE.md with timestamp testing
- ✅ Unified field naming to `submitted_at` across all files
- ✅ Added date formatting: `YYYY-MM-DD HH:MM:SS`

### v1.0 (2025-10-12)
- ✅ Complete student interface redesign
- ✅ Fixed dashboard template syntax errors
- ✅ Fixed course detail dictionary access issues
- ✅ Added comprehensive bilingual documentation
- ✅ Created MongoDB Atlas setup guide
- ✅ Added 30-second quick start guide

---

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
