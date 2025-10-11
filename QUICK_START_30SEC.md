# 🚀 30秒快速启动 | 30-Second Quick Start

## 中文版

### 1️⃣ 克隆项目
```bash
git clone https://github.com/COMP5241-2526Sem1/groupproject-team_3.git
cd groupproject-team_3
git checkout ZmhPre
```

### 2️⃣ 创建虚拟环境
```powershell
# Windows
python -m venv Project3
.\Project3\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv Project3
source Project3/bin/activate
```

### 3️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

### 4️⃣ 配置 .env 文件
创建 `.env` 文件，添加：
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=learning_platform
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### 5️⃣ 初始化数据库
```bash
python init_db.py
python seed_database.py
```

### 6️⃣ 启动应用
```bash
python app.py
```

### 7️⃣ 访问应用
打开浏览器: `http://localhost:5000`

### 8️⃣ 测试登录
```
学生账号: student_demo / student123
教师账号: teacher_demo / teacher123
管理员: admin / admin123
```

---

## English Version

### 1️⃣ Clone Project
```bash
git clone https://github.com/COMP5241-2526Sem1/groupproject-team_3.git
cd groupproject-team_3
git checkout ZmhPre
```

### 2️⃣ Create Virtual Environment
```powershell
# Windows
python -m venv Project3
.\Project3\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv Project3
source Project3/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure .env File
Create `.env` file with:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=learning_platform
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### 5️⃣ Initialize Database
```bash
python init_db.py
python seed_database.py
```

### 6️⃣ Start Application
```bash
python app.py
```

### 7️⃣ Access Application
Open browser: `http://localhost:5000`

### 8️⃣ Test Login
```
Student: student_demo / student123
Teacher: teacher_demo / teacher123
Admin: admin / admin123
```

---

## ⚠️ 常见问题 | Common Issues

### 问题 1: 虚拟环境激活失败 (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题 2: MongoDB 连接失败
- 检查 `.env` 文件的 `MONGO_URI`
- 确认 MongoDB Atlas 网络访问允许你的 IP
- 特殊字符需要 URL 编码

### 问题 3: 端口被占用
```powershell
# Windows
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F

# 或修改端口
# 在 app.py 最后改为: app.run(debug=True, port=5001)
```

### Issue 1: Virtual Environment Activation Failed (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 2: MongoDB Connection Failed
- Check `MONGO_URI` in `.env` file
- Confirm MongoDB Atlas allows your IP
- Special characters need URL encoding

### Issue 3: Port Already in Use
```powershell
# Windows
netstat -ano | findstr :5000
taskkill /PID <ProcessID> /F

# Or change port
# In app.py last line: app.run(debug=True, port=5001)
```

---

## 📱 项目功能 | Project Features

### 学生界面 | Student Interface
- ✅ Dashboard (学习统计)
- ✅ My Courses (我的课程)
- ✅ Browse Courses (浏览课程)
- ✅ Course Details (课程详情)
- ✅ My Activities (我的活动)
- ✅ Participate (参与活动)
- 🔄 Leaderboard (排行榜 - 占位)

### 教师界面 | Teacher Interface
- ✅ Course Management (课程管理)
- ✅ Create Course (创建课程)
- ✅ Create Activity (创建活动)
- ✅ View Students (查看学生)
- ✅ AI Generation (AI 生成内容)

### 管理员界面 | Admin Interface
- ✅ User Management (用户管理)
- ✅ System Overview (系统总览)

---

## 📂 项目结构 | Project Structure

```
groupproject-team_3/
├── app.py              # 入口 | Entry point
├── config.py           # 配置 | Configuration
├── .env                # 环境变量 | Environment (create this!)
├── models/             # 数据模型 | Data models
├── routes/             # 路由 | Routes
├── services/           # 服务 | Services
├── templates/          # 模板 | Templates
│   └── student/       # 学生界面 | Student UI
└── static/            # 静态文件 | Static files
    └── css/
```

---

## 🔗 相关文档 | Related Documentation

- 📘 **完整指南**: `QUICK_START_GUIDE.md`
- 🐛 **错误修复**: `DASHBOARD_COURSE_DETAIL_FIX.md`
- 🎨 **界面设计**: `STUDENT_INTERFACE_FINAL.md`
- 🧪 **测试指南**: `TESTING_COMPLETE_GUIDE.md`

---

## ✅ 安装检查 | Installation Checklist

- [ ] Python 3.8+ 已安装 | Python 3.8+ installed
- [ ] Git 已安装 | Git installed
- [ ] 项目已克隆 | Project cloned
- [ ] 虚拟环境已激活 | Virtual environment activated
- [ ] 依赖已安装 | Dependencies installed
- [ ] .env 文件已配置 | .env configured
- [ ] 数据库已初始化 | Database initialized
- [ ] 应用运行成功 | Application running
- [ ] 可以登录 | Can login

---

**需要帮助？ | Need Help?**  
查看完整指南: `QUICK_START_GUIDE.md`
