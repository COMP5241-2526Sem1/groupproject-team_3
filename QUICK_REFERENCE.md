# 🚀 Quick Reference Guide / 快速参考指南

## 📦 项目已包含的所有文件 / All Included Files

```
✅ 核心应用文件 / Core Application Files
├── app.py                      # Flask 主应用
├── config.py                   # 配置管理
├── init_db.py                  # 数据库初始化
├── requirements.txt            # Python 依赖

✅ 配置文件 / Configuration Files  
├── .env                        # 环境变量(需配置)
├── .env.example               # 环境变量模板
├── .gitignore                 # Git 忽略规则

✅ 数据模型 / Data Models (4 files)
├── models/
│   ├── user.py                # 用户模型
│   ├── course.py              # 课程模型
│   ├── student.py             # 学生模型
│   └── activity.py            # 活动模型

✅ 服务层 / Services (3 files)
├── services/
│   ├── db_service.py          # 数据库服务
│   ├── auth_service.py        # 认证服务
│   └── genai_service.py       # AI 服务(GPT-4)

✅ 路由层 / Routes (4 files)
├── routes/
│   ├── auth_routes.py         # 认证路由
│   ├── course_routes.py       # 课程路由
│   ├── activity_routes.py     # 活动路由
│   └── admin_routes.py        # 管理路由

✅ 前端静态文件 / Frontend Static Files
├── static/
│   ├── css/
│   │   └── style.css          # 响应式样式表
│   └── js/
│       └── main.js            # 前端 JavaScript

✅ HTML 模板 / HTML Templates (11 files)
├── templates/
│   ├── base.html              # 基础模板
│   ├── login.html             # 登录页
│   ├── register.html          # 注册页
│   ├── dashboard.html         # 教师仪表盘
│   ├── course_detail.html     # 课程详情
│   ├── create_course.html     # 创建课程
│   ├── create_activity.html   # 创建活动
│   ├── activity_detail.html   # 活动详情
│   ├── student_activity.html  # 学生参与页
│   ├── admin.html             # 管理仪表盘
│   └── error.html             # 错误页面

✅ 文档和工具 / Documentation & Tools
├── README.md                   # 项目说明(英文)
├── SETUP_GUIDE.md             # 详细安装指南
├── TESTING_CHECKLIST.md       # 测试清单
├── PROJECT_DELIVERY.md        # 项目交付文档(中英)
├── start.ps1                  # PowerShell 快速启动脚本
└── sample_students.csv        # 示例学生数据
```

**总计**: 35+ 个文件，完整的全栈应用！

---

## ⚡ 3 分钟快速启动 / 3-Minute Quick Start

### Step 1: 安装依赖 (30 秒)
```powershell
pip install -r requirements.txt
```

### Step 2: 配置 API (1 分钟)
编辑 `.env` 文件，填入:
1. MongoDB 连接字符串
2. OpenAI API 密钥

### Step 3: 初始化数据库 (30 秒)
```powershell
python init_db.py
```

### Step 4: 启动应用 (10 秒)
```powershell
python app.py
```

### Step 5: 访问应用 (10 秒)
打开浏览器: `http://localhost:5000`

**登录**: admin / admin123

✅ **完成！开始使用！**

---

## 🔑 关键 API 凭证获取 / Get API Credentials

### MongoDB Cloud (免费)
1. 访问: https://www.mongodb.com/cloud/atlas
2. 注册 → 创建免费集群(M0)
3. Connect → Drivers → 复制连接字符串
4. 替换 `<password>` 和数据库名
5. 粘贴到 `.env` 的 `MONGODB_URI`

### OpenAI API (付费，新用户有免费额度)
1. 访问: https://platform.openai.com/api-keys
2. 注册 → API keys → Create new key
3. 复制密钥 (sk-proj-...)
4. 粘贴到 `.env` 的 `OPENAI_API_KEY`

---

## 📱 核心功能路由 / Core Routes

### 🔐 认证 / Authentication
- `GET /login` - 登录页面
- `POST /login` - 登录提交
- `GET /register` - 注册页面
- `POST /register` - 注册提交
- `GET /logout` - 登出

### 👨‍🏫 教师功能 / Teacher Features
- `GET /dashboard` - 教师仪表盘
- `POST /course/create` - 创建课程
- `GET /course/<id>` - 课程详情
- `POST /course/<id>/import-students` - 导入学生
- `POST /activity/create` - 创建活动
- `POST /activity/ai-generate` - AI 生成活动
- `GET /activity/<id>` - 活动详情
- `POST /activity/<id>/group-answers` - AI 分组答案

### 👥 学生功能 / Student Features
- `GET /a/<link>` - 学生活动页面(无需登录)
- `POST /activity/<id>/submit` - 提交响应

### 👑 管理员功能 / Admin Features
- `GET /admin` - 管理员仪表盘
- `GET /admin/stats` - 系统统计

---

## 🎯 快速测试流程 / Quick Test Flow

### 作为教师 / As Teacher
```
1. 注册 (/register)
   ↓
2. 创建课程 (Dashboard → New Course)
   ↓
3. 导入学生 (Course Detail → Import Students)
   ↓
4. 创建活动 (Dashboard → New Activity)
   - 尝试 AI 生成: 输入 "TCP/IP protocol"
   ↓
5. 复制活动链接
   ↓
6. 在新窗口/手机上打开链接
   ↓
7. 提交响应
   ↓
8. 查看结果 (Activity Detail)
   - 简答题: 点击 "Group Answers with AI"
```

### 作为管理员 / As Admin
```
1. 登录 admin/admin123
   ↓
2. 查看统计数据
   ↓
3. 浏览教师账号
   ↓
4. 查看活动分布
```

---

## 🐛 常见问题速查 / Quick Troubleshooting

| 问题 | 解决方案 |
|------|----------|
| **ModuleNotFoundError** | `pip install -r requirements.txt` |
| **MongoDB connection failed** | 检查 `.env` 中的 `MONGODB_URI`<br>验证 IP 白名单 |
| **OpenAI API error** | 检查 `.env` 中的 `OPENAI_API_KEY`<br>查看 API 额度 |
| **Port 5000 in use** | 修改 `.env`: `APP_PORT=5001` |
| **Admin can't login** | 运行 `python init_db.py` 创建管理员 |
| **Pages not loading** | 确保 Flask 应用正在运行 |
| **AI features not working** | 验证 OpenAI API 密钥和额度 |

---

## 📊 数据库集合结构 / Database Collections

### users (用户表)
```json
{
  "username": "teacher1",
  "password": "hashed_password",
  "email": "teacher@edu.hk",
  "role": "teacher|admin",
  "institution": "HKU",
  "created_at": "2025-10-12T10:00:00",
  "last_login": "2025-10-12T11:00:00"
}
```

### courses (课程表)
```json
{
  "name": "CS101",
  "code": "COMP101",
  "teacher_id": "teacher_objectid",
  "description": "Intro to CS",
  "students": ["student_id_1", "student_id_2"],
  "created_at": "2025-10-12T10:00:00"
}
```

### activities (活动表)
```json
{
  "title": "TCP/IP Quiz",
  "type": "poll|short_answer|word_cloud",
  "content": {
    "question": "What is TCP?",
    "options": ["A", "B", "C"]
  },
  "course_id": "course_objectid",
  "teacher_id": "teacher_objectid",
  "link": "abc123xyz",
  "responses": [],
  "ai_generated": true
}
```

### students (学生表)
```json
{
  "student_id": "S001",
  "name": "Alice",
  "course_id": "course_objectid",
  "email": "alice@student.edu"
}
```

---

## 🎨 主要 CSS 类 / Main CSS Classes

### 布局 / Layout
- `.container` - 主容器
- `.card` - 卡片容器
- `.grid`, `.grid-2`, `.grid-3` - 网格布局

### 按钮 / Buttons
- `.btn` - 基础按钮
- `.btn-primary` - 主要按钮(蓝色)
- `.btn-success` - 成功按钮(绿色)
- `.btn-danger` - 危险按钮(红色)
- `.btn-sm` - 小按钮

### 表单 / Forms
- `.form-group` - 表单组
- `.form-label` - 表单标签
- `.form-control` - 表单控件

### 提示 / Alerts
- `.alert-success` - 成功提示
- `.alert-danger` - 错误提示
- `.alert-info` - 信息提示
- `.alert-warning` - 警告提示

---

## 🔧 主要 JavaScript 函数 / Main JS Functions

```javascript
// API 调用
apiCall(url, method, data)

// 显示提示
showAlert(message, type)

// 模态框
openModal(modalId)
closeModal(modalId)

// 表单验证
validateForm(formId)

// 复制活动链接
copyActivityLink(link)

// 导出表格
exportTableToCSV(tableId, filename)

// 字符计数
setupCharCounter(textareaId, counterId, maxChars)
```

---

## 📱 响应式断点 / Responsive Breakpoints

- **Mobile**: < 768px (iPhone, Android)
- **Tablet**: 769px - 1024px (iPad)
- **Desktop**: > 1024px (PC, Laptop)

所有页面已针对这三个断点优化！

---

## 🌟 AI 功能示例 / AI Feature Examples

### 生成活动 / Generate Activity
```javascript
// 前端调用
const result = await apiCall('/activity/ai-generate', 'POST', {
    course_id: 'course_id_here',
    type: 'short_answer',
    teaching_content: 'TCP/IP protocol and three-way handshake'
});

// AI 返回结果示例
{
    "questions": [
        {
            "question": "Explain the three-way handshake in TCP",
            "key_points": ["SYN", "SYN-ACK", "ACK"],
            "word_limit": 150
        }
    ]
}
```

### 分组答案 / Group Answers
```javascript
// 前端调用
const result = await apiCall('/activity/123/group-answers', 'POST');

// AI 返回结果示例
{
    "groups": [
        {
            "group_id": 1,
            "theme": "Correct understanding of handshake",
            "understanding_level": "high",
            "answers": [...]
        }
    ],
    "overall_analysis": "Most students understand the concept",
    "common_misconceptions": ["Confused TCP with UDP"]
}
```

---

## 📄 CSV 导入格式 / CSV Import Format

**student_import.csv**
```csv
student_id,name,email
S001,Alice Wong,alice@student.edu
S002,Bob Chen,bob@student.edu
S003,Charlie Lee,charlie@student.edu
```

**要求 / Requirements:**
- 必须包含表头行
- `student_id` 和 `name` 必填
- `email` 可选
- UTF-8 编码

---

## 🎓 项目特色 / Project Highlights

✨ **完整全栈应用**: 从数据库到前端完整实现  
✨ **AI 深度集成**: GPT-4 智能生成和分析  
✨ **响应式设计**: 完美适配移动端和桌面端  
✨ **清晰架构**: MVC 模式，易于维护  
✨ **安全可靠**: 密码加密，会话管理  
✨ **文档完善**: 中英双语，详细全面  
✨ **开箱即用**: 配置简单，快速部署  

---

## 📞 获取帮助 / Get Help

### 查看文档 / Check Documentation
1. `README.md` - 项目概述
2. `SETUP_GUIDE.md` - 安装指南(最详细)
3. `TESTING_CHECKLIST.md` - 测试清单
4. `PROJECT_DELIVERY.md` - 项目交付文档

### 调试技巧 / Debug Tips
1. 查看终端输出(错误信息)
2. 检查 `.env` 配置
3. 测试 MongoDB 连接
4. 验证 OpenAI API 密钥
5. 查看浏览器控制台(F12)

### 检查状态 / Check Status
```powershell
# Python 版本
python --version

# 依赖包
pip list

# 数据库连接
python -c "from services.db_service import db_service; print('OK')"

# OpenAI API
python -c "from services.genai_service import genai_service; print('OK')"
```

---

## 🚀 准备部署 / Ready to Deploy

系统已经 **production-ready**！

部署前检查:
- [ ] `.env` 配置正确
- [ ] MongoDB 连接稳定
- [ ] OpenAI API 有额度
- [ ] 修改默认管理员密码
- [ ] 设置 `FLASK_ENV=production`
- [ ] 配置 HTTPS(推荐)

---

**最后更新 / Last Updated:** 2025-10-12  
**版本 / Version:** 1.0.0  
**状态 / Status:** ✅ Ready to Use

🎉 **祝使用愉快！Happy Coding!** 🎉
