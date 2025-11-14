# 快速使用指南 | Quick Start Guide

[中文](#中文指南) | [English](#english-guide)

---

## 中文指南

### 📋 目录
1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [配置说明](#配置说明)
4. [运行程序](#运行程序)
5. [测试账号](#测试账号)
6. [常见问题](#常见问题)

---

### 🖥️ 系统要求

#### 必需软件
- **Python**: 3.8 或更高版本
- **Git**: 最新版本
- **MongoDB**: 云端 MongoDB Atlas 账号 (或本地 MongoDB 4.0+)
- **浏览器**: Chrome, Firefox, Edge 或 Safari

#### 推荐配置
- **操作系统**: Windows 10/11, macOS 10.15+, 或 Ubuntu 20.04+
- **内存**: 4GB 以上
- **磁盘空间**: 500MB 可用空间

---

### 📥 安装步骤

#### 步骤 1: 克隆项目

```bash
# 克隆仓库
git clone https://github.com/COMP5241-2526Sem1/groupproject-team_3.git

# 进入项目目录
cd groupproject-team_3

# 切换到 ZmhPre 分支
git checkout ZmhPre
```

#### 步骤 2: 创建虚拟环境

**Windows (PowerShell)**:
```powershell
# 创建虚拟环境
python -m venv Project3

# 激活虚拟环境
.\Project3\Scripts\Activate.ps1

# 如果遇到执行策略错误，运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux**:
```bash
# 创建虚拟环境
python3 -m venv Project3

# 激活虚拟环境
source Project3/bin/activate
```

#### 步骤 3: 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

**依赖包列表** (requirements.txt):
```
Flask==3.0.0
pymongo==4.15.3
python-dotenv==1.0.0
bcrypt==4.0.1
openai==1.3.0
```

---

### ⚙️ 配置说明

#### 步骤 1: 创建配置文件

在项目根目录创建 `.env` 文件:

```bash
# Windows
New-Item -Path .env -ItemType File

# macOS/Linux
touch .env
```

#### 步骤 2: 配置环境变量

编辑 `.env` 文件，添加以下内容:

```env
# MongoDB 配置
MONGODB_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/
DB_NAME=learning_platform

# Flask 配置
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# GitHub Models API 配置 (可选)
GITHUB_TOKEN=your_github_token_here
```

**重要**: 
- 将 `your_username` 和 `your_password` 替换为你的 MongoDB Atlas 凭据
- 将 `your_secret_key_here` 替换为随机密钥 (可用 `python -c "import secrets; print(secrets.token_hex(32))"` 生成)

#### 步骤 3: MongoDB Atlas 设置

1. **注册账号**: 访问 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. **创建集群**: 选择免费 M0 集群
3. **配置网络访问**: 
   - 点击 "Network Access"
   - 添加 IP 地址: `0.0.0.0/0` (允许所有访问) 或你的当前 IP
4. **创建数据库用户**:
   - 点击 "Database Access"
   - 创建用户并记录用户名和密码
5. **获取连接字符串**:
   - 点击 "Connect" → "Connect your application"
   - 复制连接字符串到 `.env` 文件的 `MONGODB_URI`

---

### 🚀 运行程序

#### 步骤 1: 初始化数据库

```bash
# 创建数据库表结构和初始数据
python init_db.py

# (可选) 添加示例课程和活动
python seed_database.py

# (可选) 创建测试账号
python create_test_accounts.py
```

#### 步骤 2: 启动应用

**方法 1 - 使用启动脚本 (推荐)**:

**Windows**:
```powershell
.\start_project3.ps1
```

**Linux/macOS**:
```bash
chmod +x start_project3.sh
./start_project3.sh
```

**方法 2 - 手动启动**:
```bash
# 确保虚拟环境已激活
python app.py
```

#### 步骤 3: 访问应用

打开浏览器，访问:
```
http://localhost:5000
```

**应该看到登录页面** ✅

---

### 👥 测试账号

#### 管理员账号
```
用户名: admin
密码: admin123
角色: 管理员 (可管理所有用户和课程)
```

#### 教师账号
```
用户名: teacher_demo
密码: teacher123
角色: 教师 (可创建课程和活动)

用户名: teacher_jane
密码: teacher123
角色: 教师
```

#### 学生账号
```
用户名: student_demo
密码: student123
角色: 学生 (学习界面)

用户名: student_alice
密码: student123
角色: 学生

用户名: student_bob
密码: student123
角色: 学生
```

---

### 🧪 功能测试

#### 学生功能测试流程

1. **登录**: 使用 `student_demo` / `student123`
2. **查看 Dashboard**: 
   - 应显示学习统计卡片
   - 显示已选课程列表
   - 显示最近活动
3. **浏览课程**: 
   - 点击 "Browse Courses"
   - 选择课程点击 "Enroll"
4. **查看课程详情**:
   - 进入 "My Courses"
   - 点击 "View Details"
   - 查看课程活动列表
5. **参与活动**:
   - 点击活动的 "Participate"
   - 提交答案或投票

#### 教师功能测试流程

1. **登录**: 使用 `teacher_demo` / `teacher123`
2. **创建课程**:
   - 点击 "Create New Course"
   - 填写课程信息并提交
3. **创建活动**:
   - 进入课程详情
   - 点击 "Create New Activity"
   - 选择活动类型 (投票/简答/词云)
   - 填写内容并保存

---

### ❓ 常见问题

#### 1. 虚拟环境激活失败 (Windows)

**错误**: `无法加载文件 Activate.ps1，因为在此系统上禁止运行脚本`

**解决方案**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. MongoDB 连接失败

**错误**: `ServerSelectionTimeoutError`

**解决方案**:
- 检查 `.env` 文件中的 `MONGODB_URI` 是否正确
- 确认 MongoDB Atlas 网络访问设置允许你的 IP
- 检查用户名和密码是否正确 (密码中的特殊字符需要 URL 编码)

#### 3. 端口 5000 已被占用

**错误**: `Address already in use`

**解决方案**:
```bash
# Windows - 查找并终止进程
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F

# Linux/macOS - 查找并终止进程
lsof -i :5000
kill -9 <PID>

# 或者修改端口 (在 app.py 最后一行)
app.run(debug=True, port=5001)
```

#### 4. 依赖安装失败

**错误**: `pip install` 报错

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像 (中国用户)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 单独安装失败的包
pip install Flask==3.0.0
```

#### 5. 页面显示 ERROR

**可能原因**:
- 数据库未初始化
- 数据格式不匹配

**解决方案**:
```bash
# 重新初始化数据库
python init_db.py
python seed_database.py

# 检查终端错误日志
# Flask 会显示详细的错误信息
```

---

### 📚 项目结构

```
groupproject-team_3/
├── app.py                 # 主应用入口
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖
├── .env                   # 环境变量 (需创建)
├── models/                # 数据模型
│   ├── user.py
│   ├── course.py
│   ├── activity.py
│   └── student.py
├── routes/                # 路由处理
│   ├── auth_routes.py
│   ├── admin_routes.py
│   ├── course_routes.py
│   ├── activity_routes.py
│   └── student_routes.py
├── services/              # 业务逻辑
│   ├── auth_service.py
│   ├── db_service.py
│   └── genai_service.py
├── templates/             # HTML 模板
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── student/          # 学生界面
│       ├── dashboard.html
│       ├── my_courses.html
│       ├── browse_courses.html
│       └── course_detail.html
└── static/               # 静态资源
    ├── css/
    │   └── student.css
    └── js/
```

---

### 🔧 开发工具

#### 推荐的 IDE/编辑器
- **VS Code** (推荐)
  - 安装 Python 扩展
  - 安装 Pylance 扩展
- **PyCharm**
- **Sublime Text**

#### 调试模式

Flask 已启用调试模式，修改代码后会自动重载:
```python
# app.py 最后一行
app.run(debug=True)
```

#### 查看日志

终端会实时显示:
- HTTP 请求日志
- 错误堆栈信息
- 数据库操作日志

---

### 📞 获取帮助

如果遇到问题:

1. **查看文档**:
   - `DASHBOARD_COURSE_DETAIL_FIX.md` - 错误修复记录
   - `STUDENT_INTERFACE_FINAL.md` - 学生界面文档
   - `TESTING_COMPLETE_GUIDE.md` - 测试指南

2. **检查日志**: 查看终端输出的错误信息

3. **GitHub Issues**: 在仓库中创建 Issue

4. **联系团队**: 联系项目维护者

---

### ✅ 安装检查清单

- [ ] Python 3.8+ 已安装
- [ ] Git 已安装
- [ ] 项目已克隆到本地
- [ ] 虚拟环境已创建并激活
- [ ] 依赖包已安装 (`pip list` 检查)
- [ ] `.env` 文件已创建并配置
- [ ] MongoDB Atlas 已设置
- [ ] 数据库已初始化 (`init_db.py`)
- [ ] 应用启动成功
- [ ] 浏览器可以访问 `http://localhost:5000`
- [ ] 可以使用测试账号登录

---

## English Guide

### 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Test Accounts](#test-accounts)
6. [Troubleshooting](#troubleshooting)

---

### 🖥️ System Requirements

#### Required Software
- **Python**: 3.8 or higher
- **Git**: Latest version
- **MongoDB**: MongoDB Atlas account (or local MongoDB 4.0+)
- **Browser**: Chrome, Firefox, Edge, or Safari

#### Recommended Specs
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 20.04+
- **RAM**: 4GB or more
- **Disk Space**: 500MB available

---

### 📥 Installation Steps

#### Step 1: Clone the Project

```bash
# Clone the repository
git clone https://github.com/COMP5241-2526Sem1/groupproject-team_3.git

# Navigate to project directory
cd groupproject-team_3

# Switch to ZmhPre branch
git checkout ZmhPre
```

#### Step 2: Create Virtual Environment

**Windows (PowerShell)**:
```powershell
# Create virtual environment
python -m venv Project3

# Activate virtual environment
.\Project3\Scripts\Activate.ps1

# If you encounter execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux**:
```bash
# Create virtual environment
python3 -m venv Project3

# Activate virtual environment
source Project3/bin/activate
```

#### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

**Dependencies List** (requirements.txt):
```
Flask==3.0.0
pymongo==4.15.3
python-dotenv==1.0.0
bcrypt==4.0.1
openai==1.3.0
```

---

### ⚙️ Configuration

#### Step 1: Create Configuration File

Create a `.env` file in the project root:

```bash
# Windows
New-Item -Path .env -ItemType File

# macOS/Linux
touch .env
```

#### Step 2: Configure Environment Variables

Edit `.env` file and add:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/
DB_NAME=learning_platform

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# GitHub Models API (Optional)
GITHUB_TOKEN=your_github_token_here
```

**Important**: 
- Replace `your_username` and `your_password` with your MongoDB Atlas credentials
- Replace `your_secret_key_here` with a random key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)

#### Step 3: MongoDB Atlas Setup

1. **Sign Up**: Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. **Create Cluster**: Choose free M0 tier
3. **Configure Network Access**: 
   - Click "Network Access"
   - Add IP: `0.0.0.0/0` (allow all) or your current IP
4. **Create Database User**:
   - Click "Database Access"
   - Create user and note username/password
5. **Get Connection String**:
   - Click "Connect" → "Connect your application"
   - Copy connection string to `MONGODB_URI` in `.env`

---

### 🚀 Running the Application

#### Step 1: Initialize Database

```bash
# Create database schema and initial data
python init_db.py

# (Optional) Add sample courses and activities
python seed_database.py

# (Optional) Create test accounts
python create_test_accounts.py
```

#### Step 2: Start Application

**Method 1 - Using Start Script (Recommended)**:

**Windows**:
```powershell
.\start_project3.ps1
```

**Linux/macOS**:
```bash
chmod +x start_project3.sh
./start_project3.sh
```

**Method 2 - Manual Start**:
```bash
# Make sure virtual environment is activated
python app.py
```

#### Step 3: Access Application

Open browser and visit:
```
http://localhost:5000
```

**You should see the login page** ✅

---

### 👥 Test Accounts

#### Administrator Account
```
Username: admin
Password: admin123
Role: Administrator (manage all users and courses)
```

#### Teacher Accounts
```
Username: teacher_demo
Password: teacher123
Role: Teacher (create courses and activities)

Username: teacher_jane
Password: teacher123
Role: Teacher
```

#### Student Accounts
```
Username: student_demo
Password: student123
Role: Student (learning interface)

Username: student_alice
Password: student123
Role: Student

Username: student_bob
Password: student123
Role: Student
```

---

### 🧪 Feature Testing

#### Student Features Test Flow

1. **Login**: Use `student_demo` / `student123`
2. **View Dashboard**: 
   - Should display learning statistics cards
   - Show enrolled courses list
   - Show recent activities
3. **Browse Courses**: 
   - Click "Browse Courses"
   - Select course and click "Enroll"
4. **View Course Details**:
   - Go to "My Courses"
   - Click "View Details"
   - See course activities list
5. **Participate in Activities**:
   - Click activity "Participate"
   - Submit answers or votes

#### Teacher Features Test Flow

1. **Login**: Use `teacher_demo` / `teacher123`
2. **Create Course**:
   - Click "Create New Course"
   - Fill in course information and submit
3. **Create Activity**:
   - Enter course details
   - Click "Create New Activity"
   - Choose activity type (poll/short answer/word cloud)
   - Fill content and save

---

### ❓ Troubleshooting

#### 1. Virtual Environment Activation Failed (Windows)

**Error**: `Cannot load file Activate.ps1 because running scripts is disabled`

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. MongoDB Connection Failed

**Error**: `ServerSelectionTimeoutError`

**Solution**:
- Check `MONGODB_URI` in `.env` file is correct
- Verify MongoDB Atlas network access allows your IP
- Confirm username/password are correct (special characters need URL encoding)

#### 3. Port 5000 Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <ProcessID> /F

# Linux/macOS - Find and kill process
lsof -i :5000
kill -9 <PID>

# Or change port (in app.py last line)
app.run(debug=True, port=5001)
```

#### 4. Dependencies Installation Failed

**Error**: `pip install` errors

**Solution**:
```bash
# Upgrade pip
pip install --upgrade pip

# Use mirror (for users in China)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install failed packages individually
pip install Flask==3.0.0
```

#### 5. Page Shows ERROR

**Possible Causes**:
- Database not initialized
- Data format mismatch

**Solution**:
```bash
# Re-initialize database
python init_db.py
python seed_database.py

# Check terminal error logs
# Flask will show detailed error messages
```

---

### 📚 Project Structure

```
groupproject-team_3/
├── app.py                 # Main application entry
├── config.py              # Configuration file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── models/                # Data models
│   ├── user.py
│   ├── course.py
│   ├── activity.py
│   └── student.py
├── routes/                # Route handlers
│   ├── auth_routes.py
│   ├── admin_routes.py
│   ├── course_routes.py
│   ├── activity_routes.py
│   └── student_routes.py
├── services/              # Business logic
│   ├── auth_service.py
│   ├── db_service.py
│   └── genai_service.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── student/          # Student interface
│       ├── dashboard.html
│       ├── my_courses.html
│       ├── browse_courses.html
│       └── course_detail.html
└── static/               # Static assets
    ├── css/
    │   └── student.css
    └── js/
```

---

### 🔧 Development Tools

#### Recommended IDE/Editors
- **VS Code** (Recommended)
  - Install Python extension
  - Install Pylance extension
- **PyCharm**
- **Sublime Text**

#### Debug Mode

Flask debug mode is enabled, auto-reloads on code changes:
```python
# Last line in app.py
app.run(debug=True)
```

#### View Logs

Terminal shows real-time:
- HTTP request logs
- Error stack traces
- Database operation logs

---

### 📞 Getting Help

If you encounter issues:

1. **Check Documentation**:
   - `DASHBOARD_COURSE_DETAIL_FIX.md` - Error fix records
   - `STUDENT_INTERFACE_FINAL.md` - Student interface docs
   - `TESTING_COMPLETE_GUIDE.md` - Testing guide

2. **Check Logs**: View error messages in terminal output

3. **GitHub Issues**: Create an issue in the repository

4. **Contact Team**: Reach out to project maintainers

---

### ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Project cloned locally
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (check with `pip list`)
- [ ] `.env` file created and configured
- [ ] MongoDB Atlas configured
- [ ] Database initialized (`init_db.py`)
- [ ] Application starts successfully
- [ ] Browser can access `http://localhost:5000`
- [ ] Can login with test accounts

---

## 🎯 Quick Commands Reference

### Start Application (启动应用)
```bash
# Windows
.\Project3\Scripts\Activate.ps1
python app.py

# macOS/Linux
source Project3/bin/activate
python app.py
```

### Stop Application (停止应用)
```
Press Ctrl+C in terminal
```

### Reset Database (重置数据库)
```bash
python init_db.py
python seed_database.py
```

### Update Dependencies (更新依赖)
```bash
pip install -r requirements.txt --upgrade
```

---

## 📖 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **MongoDB Documentation**: https://docs.mongodb.com/
- **Python Documentation**: https://docs.python.org/3/

---

**Last Updated**: 2025-10-12  
**Version**: 1.0  
**Branch**: ZmhPre  
**Maintainer**: Team 3
