# 📚 Learning Activity Management System - 用户手册

## 目录

1. [系统概述](#系统概述)
2. [系统架构](#系统架构)
3. [数据库设计](#数据库设计)
4. [用户角色与权限](#用户角色与权限)
5. [功能详解](#功能详解)
   - [管理员功能](#管理员功能)
   - [教师功能](#教师功能)
   - [学生功能](#学生功能)
6. [使用指南](#使用指南)
7. [常见问题](#常见问题)

---

## 系统概述

### 项目简介

Learning Activity Management System 是一个基于 Web 的教育管理平台,旨在促进师生互动,提供智能化的学习活动管理功能。系统支持多种活动类型,并集成了 AI 辅助功能。

### 核心特性

- ✅ **多角色支持**: 管理员、教师、学生三种角色
- 🤖 **AI 驱动**: 集成 GPT-4o-mini,支持活动自动生成和智能评估
- 📊 **多种活动类型**: Poll(投票)、Short Answer(简答题)、Word Cloud(词云)
- 🎮 **游戏化设计**: 积分系统、排行榜、徽章奖励
- 📱 **响应式界面**: 支持桌面和移动设备
- 🔐 **安全可靠**: 密码加密、会话管理、权限控制

### 技术栈

**后端**:
- Python 3.13
- Flask 3.0.0
- MongoDB (NoSQL 数据库)
- OpenAI GPT-4o-mini (AI 服务)

**前端**:
- HTML5 + CSS3
- JavaScript (ES6+)
- Bootstrap 样式组件

**部署**:
- Vercel (生产环境)
- 本地开发环境支持

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                     用户层 (User Layer)                    │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  管理员   │    │   教师    │    │   学生    │          │
│  └──────────┘    └──────────┘    └──────────┘          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
┌────────────────────┴────────────────────────────────────┐
│                  表现层 (Presentation Layer)              │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Flask Templates (Jinja2)                 │   │
│  │  ┌─────────┐ ┌─────────┐ ┌──────────┐           │   │
│  │  │ Admin UI│ │Teacher UI│ │Student UI│           │   │
│  │  └─────────┘ └─────────┘ └──────────┘           │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                  应用层 (Application Layer)               │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Flask Application                   │   │
│  │  ┌─────────────────────────────────────────┐    │   │
│  │  │         Routes (Blueprints)             │    │   │
│  │  │  • admin_routes  • activity_routes      │    │   │
│  │  │  • auth_routes   • course_routes        │    │   │
│  │  │  • student_routes                       │    │   │
│  │  └─────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                  业务层 (Business Layer)                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Services                            │   │
│  │  • auth_service     (认证服务)                    │   │
│  │  • genai_service    (AI 服务)                     │   │
│  │  • points_service   (积分服务)                    │   │
│  │  • document_service (文档服务)                    │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                  数据层 (Data Layer)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Models (数据模型)                     │   │
│  │  • User      • Course    • Activity              │   │
│  │  • Student   • Response                          │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │           MongoDB Database                       │   │
│  │  Collections: users, courses, activities,        │   │
│  │              students, responses                 │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                  外部服务 (External Services)             │
│  ┌──────────────────────────────────────────────────┐   │
│  │  OpenAI API (GPT-4o-mini)                        │   │
│  │  • 活动内容生成                                     │   │
│  │  • 学生答案评估                                     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 目录结构

```
groupproject-team_3/
├── app.py                      # Flask 应用入口
├── config.py                   # 配置文件
├── requirements.txt            # Python 依赖
├── vercel.json                 # Vercel 部署配置
│
├── models/                     # 数据模型层
│   ├── user.py                 # 用户模型
│   ├── course.py               # 课程模型
│   ├── activity.py             # 活动模型
│   └── student.py              # 学生模型
│
├── routes/                     # 路由层 (Blueprints)
│   ├── auth_routes.py          # 认证路由
│   ├── admin_routes.py         # 管理员路由
│   ├── course_routes.py        # 课程路由
│   ├── activity_routes.py      # 活动路由
│   └── student_routes.py       # 学生路由
│
├── services/                   # 业务逻辑层
│   ├── auth_service.py         # 认证服务
│   ├── db_service.py           # 数据库服务
│   ├── genai_service.py        # AI 服务
│   ├── points_service.py       # 积分服务
│   └── document_service.py     # 文档服务
│
├── templates/                  # HTML 模板
│   ├── base.html               # 基础模板
│   ├── index.html              # 首页
│   ├── login.html              # 登录页
│   │
│   ├── admin.html              # 管理员仪表盘
│   ├── admin_users.html        # 用户管理
│   ├── admin_activities.html   # 活动管理
│   ├── admin_courses.html      # 课程管理
│   │
│   ├── dashboard.html          # 教师仪表盘
│   ├── create_course.html      # 创建课程
│   ├── create_activity.html    # 创建活动
│   ├── activity_detail.html    # 活动详情
│   │
│   └── student/                # 学生模板
│       ├── dashboard.html      # 学生仪表盘
│       ├── activity.html       # 参与活动
│       ├── leaderboard.html    # 排行榜
│       └── profile.html        # 个人资料
│
├── static/                     # 静态资源
│   ├── css/
│   │   └── style.css           # 全局样式
│   └── js/
│       └── main.js             # 全局脚本
│
└── uploads/                    # 文件上传目录
```

---

## 数据库设计

### MongoDB Collections

#### 1. Users Collection (用户集合)

存储系统中所有用户的信息(管理员、教师)。

```javascript
{
  _id: ObjectId("..."),
  username: "teacher_john",           // 用户名(唯一)
  email: "john@university.edu",       // 邮箱
  password_hash: "...",               // 密码哈希(bcrypt)
  role: "teacher",                    // 角色: admin / teacher
  institution: "ABC University",      // 所属机构
  created_at: ISODate("2025-01-15"),  // 创建时间
  last_login: ISODate("2025-11-13"),  // 最后登录时间
  active: true                        // 账户状态
}
```

**索引**:
- `username`: 唯一索引
- `email`: 唯一索引
- `role`: 普通索引

#### 2. Courses Collection (课程集合)

存储教师创建的课程信息。

```javascript
{
  _id: ObjectId("..."),
  name: "Introduction to Python",     // 课程名称
  code: "CS101",                      // 课程代码(唯一)
  description: "Learn Python basics", // 课程描述
  teacher_id: "68f2087d...",          // 教师ID(外键)
  students: ["student_id1", ...],     // 注册学生ID列表
  created_at: ISODate("2025-09-01"),  // 创建时间
  updated_at: ISODate("2025-11-13"),  // 更新时间
  active: true                        // 课程状态
}
```

**索引**:
- `code`: 唯一索引
- `teacher_id`: 普通索引
- `active`: 普通索引

#### 3. Activities Collection (活动集合)

存储各类学习活动的详细信息。

```javascript
{
  _id: ObjectId("..."),
  title: "Week 1 Quiz",               // 活动标题
  type: "poll",                       // 活动类型: poll / short_answer / word_cloud
  course_id: "68f2097a...",           // 课程ID(外键)
  teacher_id: "68f2087d...",          // 教师ID(外键)
  link: "a4b9c2d1",                   // 唯一访问链接
  
  // 活动内容(根据类型不同而变化)
  content: {
    // Poll 类型
    questions: [
      {
        question: "What is Python?",
        options: [
          { label: "A", text: "Programming Language" },
          { label: "B", text: "Snake" }
        ],
        correct_answer: "A"
      }
    ],
    allow_multiple: false,
    
    // Short Answer 类型
    question: "Explain inheritance in OOP",
    word_limit: 200,
    key_points: ["inheritance", "reusability", "parent-child"],
    
    // Word Cloud 类型
    question: "Keywords about Python",
    instructions: "Enter keywords related to Python"
  },
  
  responses: [                        // 学生回答列表
    {
      student_id: "2023001",
      student_name: "Alice Wang",
      answer: "...",                  // 答案内容
      submitted_at: ISODate("..."),   // 提交时间
      points_earned: 10,              // 获得积分
      ai_evaluation: {                // AI 评估(仅 SA/WC)
        score: 85,
        feedback: "Good explanation",
        strengths: ["Clear structure"],
        improvements: ["Add examples"]
      }
    }
  ],
  
  deadline: ISODate("2025-11-20"),    // 截止日期(可选)
  ai_generated: false,                // 是否AI生成
  created_at: ISODate("2025-11-10"),  // 创建时间
  updated_at: ISODate("2025-11-13"),  // 更新时间
  active: true                        // 活动状态
}
```

**索引**:
- `link`: 唯一索引
- `course_id`: 普通索引
- `teacher_id`: 普通索引
- `type`: 普通索引
- `active`: 普通索引

#### 4. Students Collection (学生集合)

存储学生的注册信息。

```javascript
{
  _id: ObjectId("..."),
  student_id: "2023001",              // 学号
  name: "Alice Wang",                 // 姓名
  email: "alice@student.edu",         // 邮箱
  course_id: "68f2097a...",           // 课程ID(外键)
  points: 150,                        // 总积分
  badges: ["first_response", ...],    // 徽章列表
  created_at: ISODate("2025-09-15")   // 注册时间
}
```

**索引**:
- `student_id + course_id`: 复合唯一索引
- `course_id`: 普通索引

### ER 图(实体关系)

```
┌──────────┐           ┌──────────┐
│  Users   │           │ Courses  │
│          │ 1      M  │          │
│ _id      ├───────────┤ _id      │
│ username │  teaches  │ name     │
│ role     │           │ code     │
│ email    │           │teacher_id│
└──────────┘           └────┬─────┘
                            │
                            │ 1
                            │
                            │ M
                       ┌────┴──────┐
                       │Activities │
                       │           │
                       │ _id       │
                       │ title     │
                       │ type      │
                       │ course_id │
                       │ responses │
                       └────┬──────┘
                            │
                            │ M
                            │
                            │ M
                       ┌────┴──────┐
                       │ Students  │
                       │           │
                       │ _id       │
                       │student_id │
                       │ name      │
                       │ course_id │
                       │ points    │
                       └───────────┘
```

### 数据关系

1. **User → Course**: 一对多(一个教师可以创建多个课程)
2. **Course → Activity**: 一对多(一个课程可以有多个活动)
3. **Course → Student**: 一对多(一个课程可以有多个学生)
4. **Activity → Response**: 一对多(一个活动可以有多个回答,嵌入式存储在 Activity 中)

---

## 用户角色与权限

### 角色定义

| 角色 | 英文 | 权限级别 | 主要功能 |
|------|------|----------|----------|
| 👑 管理员 | Admin | 最高 | 系统管理、用户管理、数据管理 |
| 👨‍🏫 教师 | Teacher | 中等 | 课程管理、活动管理、学生管理 |
| 👨‍🎓 学生 | Student | 基础 | 参与活动、查看成绩、排行榜 |

### 权限矩阵

| 功能模块 | 管理员 | 教师 | 学生 |
|---------|--------|------|------|
| **用户管理** |
| 查看所有用户 | ✅ | ❌ | ❌ |
| 创建/编辑/删除用户 | ✅ | ❌ | ❌ |
| 创建管理员账号 | ✅ | ❌ | ❌ |
| **课程管理** |
| 查看所有课程 | ✅ | ✅(仅自己) | ✅(仅注册) |
| 创建课程 | ✅ | ✅ | ❌ |
| 编辑课程 | ✅ | ✅(仅自己) | ❌ |
| 删除课程 | ✅ | ✅(仅自己) | ❌ |
| 注册课程 | ❌ | ❌ | ✅ |
| **活动管理** |
| 查看所有活动 | ✅ | ✅(仅自己) | ✅(仅注册) |
| 创建活动(手动/AI) | ✅ | ✅ | ❌ |
| 编辑活动 | ✅ | ✅(仅自己) | ❌ |
| 删除活动 | ✅ | ✅(仅自己) | ❌ |
| 参与活动 | ❌ | ❌ | ✅ |
| 查看活动结果 | ✅ | ✅(仅自己) | ✅(仅自己) |
| **学生管理** |
| 导入学生 | ❌ | ✅ | ❌ |
| 查看学生列表 | ✅ | ✅(仅自己课程) | ❌ |
| 查看学生成绩 | ✅ | ✅(仅自己课程) | ✅(仅自己) |
| **积分系统** |
| 查看排行榜 | ❌ | ✅ | ✅ |
| 手动调整积分 | ✅ | ❌ | ❌ |
| **AI 功能** |
| AI 生成活动 | ❌ | ✅ | ❌ |
| AI 评估答案 | ❌ | ✅ | ✅(查看) |

---

## 功能详解

### 管理员功能

#### 1. 管理员仪表盘

**访问路径**: `/admin`

**主要功能**:
- 📊 系统统计信息
  - 教师总数
  - 活动总数
  - 学生总数
- 📈 活动类型分布
  - Poll 数量
  - Short Answer 数量
  - Word Cloud 数量
- 👥 最近注册的教师列表

**界面元素**:
```
┌─────────────────────────────────────────────┐
│  🎯 Quick Actions                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │👥 Manage│ │📝 Manage│ │📚 View  │       │
│  │  Users  │ │Activities│ │ Courses │       │
│  └─────────┘ └─────────┘ └─────────┘       │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  Statistics Overview                         │
│  [150 Teachers] [1,234 Activities] [3,456...│
└─────────────────────────────────────────────┘
```

#### 2. 用户管理

**访问路径**: `/admin/users`

**主要功能**:
- 🔍 搜索用户(用户名/邮箱)
- 🔽 筛选用户(按角色)
- ➕ 创建新用户(教师/管理员)
- ✏️ 编辑用户信息
- 🗑️ 删除用户
- 👁️ 查看用户详情

**操作流程 - 创建管理员**:
1. 点击"Create Admin"按钮
2. 填写表单:
   - Username (必填)
   - Email (必填)
   - Password (必填,最少6位)
   - Institution (可选)
3. 点击"Create Admin Account"
4. 系统自动创建并显示成功消息

**操作流程 - 编辑用户**:
1. 在用户列表中找到目标用户
2. 点击"✏️ Edit"按钮
3. 在弹出的模态框中修改信息
4. 点击"Save Changes"
5. 系统更新用户信息

#### 3. 活动管理

**访问路径**: `/admin/activities-manage`

**主要功能**:
- 🔍 搜索活动(标题/课程/教师)
- 🔽 筛选活动
  - 按活动类型
  - 按教师
- 👁️ 查看活动详情
- 🗑️ 删除活动(级联删除所有回答)

**数据展示**:
- 活动标题
- 活动类型(带颜色徽章)
- 所属课程
- 创建教师
- 回答数量
- 创建时间

#### 4. 课程管理 ⭐ 新功能

**访问路径**: `/admin/courses`

**主要功能**:
- 🔍 搜索课程(名称/描述/教师)
- 🔽 筛选课程
  - 按教师
  - 按状态(活跃/归档)
- 👁️ 查看课程详情
  - 课程信息
  - 教师信息
  - 学生数量
  - 活动数量
- ✏️ 编辑课程
  - 修改课程名称
  - 修改课程描述
  - 更换教师
- 🗑️ 删除课程
  - 级联删除课程下所有活动
  - 删除所有学生注册记录
  - 删除课程本身

**安全提示**:
- 删除操作需要二次确认
- 显示将被影响的数据数量
- 操作不可逆,请谨慎使用

---

### 教师功能

#### 1. 教师仪表盘

**访问路径**: `/dashboard`

**主要功能**:
- 📊 课程统计
  - 课程数量
  - 活动数量
  - 学生总数
- 📚 课程列表
  - 课程名称和代码
  - 学生数量
  - 活动数量
  - 快速操作按钮
- ⚡ 快速操作
  - 创建新课程
  - 创建新活动
  - 查看课程详情

**界面导航**:
```
┌─────────────────────────────────────────────┐
│  Dashboard > My Courses                      │
│  [➕ New Course] [📝 New Activity]           │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  Course: Introduction to Python (CS101)      │
│  👥 45 Students | 📝 12 Activities           │
│  [View Details] [Create Activity]            │
└─────────────────────────────────────────────┘
```

#### 2. 创建课程

**访问路径**: `/course/create`

**操作步骤**:
1. 填写课程信息:
   - **Course Name** (必填): 课程名称
   - **Course Code** (必填,唯一): 课程代码,如 CS101
   - **Description** (可选): 课程描述
2. 点击"Create Course"
3. 系统生成课程并跳转到课程详情页

**注意事项**:
- 课程代码必须唯一
- 课程代码建议使用字母+数字组合
- 课程创建后可以随时添加学生

#### 3. 导入学生

**访问路径**: 课程详情页 → Import Students

**支持格式**: CSV 文件

**CSV 文件格式**:
```csv
student_id,name,email
2023001,Alice Wang,alice@student.edu
2023002,Bob Chen,bob@student.edu
2023003,Carol Li,carol@student.edu
```

**导入步骤**:
1. 准备 CSV 文件(确保格式正确)
2. 在课程详情页点击"Import Students"
3. 选择 CSV 文件
4. 点击"Upload"
5. 系统显示导入结果

**字段说明**:
- `student_id`: 学号(必填,唯一)
- `name`: 学生姓名(必填)
- `email`: 邮箱(可选,但建议填写)

#### 4. 创建活动

**访问路径**: `/activity/create`

**两种创建方式**:

##### A. 手动创建

适用于精确控制活动内容的场景。

**通用字段**:
- Course (必填): 选择课程
- Activity Type (必填): 选择活动类型
- Activity Title (必填): 活动标题
- Deadline (可选): 截止日期

**Poll (投票) 字段**:
- Question (必填): 投票问题
- Options (至少2个): 选项列表
- Allow Multiple (可选): 允许多选

**创建 Poll 示例**:
```
Title: Week 1 Knowledge Check
Question: What is the output of print(2 + 2)?
Options:
  - 22
  - 4
  - "2 + 2"
  - Error
```

**Short Answer (简答题) 字段**:
- Question (必填): 问题描述
- Word Limit (默认200): 字数限制

**创建 Short Answer 示例**:
```
Title: Explain OOP Concepts
Question: Explain the concept of inheritance in Object-Oriented Programming. Provide examples.
Word Limit: 300
```

**Word Cloud (词云) 字段**:
- Question (必填): 问题描述
- Instructions (可选): 作答说明

**创建 Word Cloud 示例**:
```
Title: Python Keywords
Question: What keywords come to mind when you think of Python programming?
Instructions: Enter keywords separated by commas
```

##### B. AI 生成 🤖

使用 GPT-4o-mini 自动生成活动内容。

**输入方式**:
1. **文本输入**: 直接输入教学内容
2. **文件上传**: 上传文档(PDF/TXT/DOCX,最大5MB)

**AI 生成步骤**:
1. 选择"AI-Assisted"标签
2. 选择课程
3. 选择活动类型
4. 选择内容来源(文本/文件)
5. 输入教学内容或上传文件
6. (Poll类型)选择题目数量(1-5)
7. 点击"Generate with AI"
8. 等待AI生成(约5-10秒)
9. 预览生成的内容
10. 确认并创建活动

**AI 生成示例 - Poll**:
```
输入: "Python is a high-level programming language known for its simplicity and readability..."

AI 输出:
Title: Python Fundamentals Quiz
Questions:
1. What is Python primarily known for?
   A. Complexity
   B. Simplicity and readability ✅
   C. Low-level operations
   D. Hardware control

2. Python is a _____ language.
   A. Low-level
   B. High-level ✅
   C. Assembly
   D. Machine
```

**AI 生成示例 - Short Answer**:
```
输入: "Object-Oriented Programming concepts including classes and inheritance..."

AI 输出:
Title: OOP Concepts Analysis
Question: Explain the key concepts of Object-Oriented Programming, focusing on classes and inheritance. Provide real-world examples to illustrate your explanation.
Key Points: classes, inheritance, objects, encapsulation, polymorphism
Word Limit: 250
```

**AI 生成特点**:
- ✅ 自动生成符合教学内容的问题
- ✅ Poll 自动包含正确答案标记
- ✅ Short Answer 自动提取关键点
- ✅ 内容质量高,符合教学标准
- ✅ 支持中英文内容

#### 5. 查看活动详情

**访问路径**: `/activity/{activity_id}`

**页面内容**:

**顶部信息卡**:
- 活动标题
- 活动类型
- 所属课程
- 创建时间
- 截止日期(如有)
- 分享链接
- 参与统计

**学生回答列表**:

**Poll 回答显示**:
```
Alice Wang (2023001)
  Answer: B. High-level ✅
  Submitted: 2025-11-13 10:30
  Points: +10
```

**Short Answer 回答显示**:
```
Bob Chen (2023002)
  Answer: "Inheritance is a fundamental concept in OOP that allows..."
  Submitted: 2025-11-13 11:15
  Points: +15
  
  [👁️ View AI Feedback] ← 点击查看AI评估
  
  AI Evaluation:
  Score: 85/100 🟢
  Feedback: "Good explanation of inheritance with clear examples."
  Strengths: ✓ Clear structure ✓ Good examples
  Improvements: • Could elaborate on method overriding
```

**Word Cloud 回答显示**:
```
Carol Li (2023003)
  Keywords: python, programming, simple, powerful, versatile
  Submitted: 2025-11-13 12:00
  Points: +10
  
  [👁️ View AI Feedback]
```

**操作按钮**:
- 🔗 Copy Link: 复制分享链接
- 📊 Export Data: 导出回答数据
- 🗑️ Delete Activity: 删除活动

#### 6. 课程详情页

**访问路径**: `/course/{course_id}`

**页面组成**:

**课程信息卡**:
- 课程名称和代码
- 课程描述
- 创建时间
- 统计数据

**学生管理区**:
- 已注册学生列表
- 学生学号、姓名、邮箱
- 积分排名
- 导入学生按钮

**活动列表**:
- 活动标题和类型
- 回答数量
- 参与率
- 创建时间
- 快速操作(查看/删除)

---

### 学生功能

#### 1. 学生仪表盘

**访问路径**: `/student/dashboard`

**主要内容**:
- 🎯 个人统计
  - 总积分
  - 已完成活动数
  - 已获得徽章
  - 排名信息
- 📝 待完成活动
  - 活动标题
  - 所属课程
  - 截止日期
  - "Start"按钮
- ⏱️ 最近提交的活动

**快速导航**:
```
┌─────────────────────────────────────────────┐
│  Welcome, Alice Wang! 🎓                     │
│  Total Points: 🪙 450                        │
│  Rank: #3 in course                          │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  📝 Pending Activities (3)                   │
│  • Week 2 Quiz - Due: Nov 15                │
│  • Python Concepts - Due: Nov 18            │
│  • OOP Discussion - Due: Nov 20             │
└─────────────────────────────────────────────┘
```

#### 2. 我的课程

**访问路径**: `/student/my-courses`

**页面功能**:
- 查看已注册的所有课程
- 显示每个课程的:
  - 课程名称和代码
  - 教师姓名
  - 活动数量
  - 个人完成进度
- 快速进入课程查看活动

#### 3. 浏览课程

**访问路径**: `/student/browse-courses`

**页面功能**:
- 查看所有可用课程
- 按课程代码注册课程
- 显示课程信息:
  - 课程名称
  - 教师
  - 描述
  - 当前学生数

**注册流程**:
1. 输入教师提供的课程代码(如 CS101)
2. 点击"Register"
3. 系统验证代码
4. 注册成功,跳转到课程页面

#### 4. 参与活动

**访问路径**: 
- 通过分享链接: `/a/{activity_link}`
- 通过我的活动: `/student/my-activities`

**参与流程**:

##### Poll 活动:
1. 阅读问题
2. 选择答案(单选或多选)
3. 点击"Submit Answer"
4. 立即查看结果:
   - ✅ 答对: 显示"Correct!"+ 积分奖励
   - ❌ 答错: 显示正确答案
5. 可以修改答案(如果教师允许)

##### Short Answer 活动:
1. 阅读问题和要求
2. 在文本框中输入答案
3. 系统显示字数统计
4. 点击"Submit Answer"
5. **AI 自动评估** 🤖:
   - 评分(0-100)
   - 详细反馈
   - 优点分析
   - 改进建议
   - 鼓励语
6. 获得积分(基于AI评分)
7. 可以重新提交获取新评估

**AI 评估示例**:
```
┌─────────────────────────────────────────────┐
│  🤖 AI Evaluation Results                    │
│                                              │
│  Score: 85/100 🟢                            │
│                                              │
│  📝 Feedback:                                │
│  "Your explanation demonstrates a solid      │
│  understanding of inheritance in OOP. The    │
│  examples are clear and relevant."           │
│                                              │
│  ✨ Strengths:                               │
│  • Clear structure and organization          │
│  • Good real-world examples                  │
│  • Correct technical terminology             │
│                                              │
│  💡 Areas for Improvement:                   │
│  • Consider discussing method overriding     │
│  • Could add more code examples              │
│                                              │
│  🌟 Keep up the great work!                  │
│                                              │
│  Points Earned: +17 🪙                       │
└─────────────────────────────────────────────┘
```

##### Word Cloud 活动:
1. 阅读问题
2. 输入关键词(用逗号分隔)
3. 点击"Submit Answer"
4. **AI 评估关键词相关性** 🤖:
   - 评估关键词质量
   - 分析概念理解
   - 提供反馈
5. 获得积分
6. 可以重新提交

#### 5. 排行榜 🏆

**访问路径**: `/student/leaderboard`

**页面内容**:
- 🥇 前三名高亮显示
- 完整排名列表:
  - 排名
  - 学生姓名
  - 总积分
  - 完成活动数
  - 徽章数量
- 个人排名高亮
- 实时更新

**排行榜规则**:
- 按总积分排序
- 积分相同按完成时间排序
- 只显示同课程学生
- 每周重置(可选)

#### 6. 个人资料

**访问路径**: `/student/profile`

**可查看/编辑**:
- 👤 基本信息
  - 学号
  - 姓名
  - 邮箱
- 📊 学习统计
  - 总积分
  - 完成活动数
  - 参与率
- 🏅 徽章展示
  - First Response (首次回答)
  - Perfect Score (满分)
  - Speed Demon (快速回答)
  - Active Learner (活跃学习者)
- 📈 积分历史

---

## 使用指南

### 快速开始

#### 教师快速指南 (5分钟)

1. **注册/登录**
   - 访问系统首页
   - 使用教师账号登录
   - 或联系管理员创建账号

2. **创建课程**
   ```
   Dashboard → ➕ New Course
   填写: 课程名称, 课程代码, 描述
   点击: Create Course
   ```

3. **导入学生**
   ```
   Course Details → Import Students
   上传 CSV 文件(student_id, name, email)
   ```

4. **创建活动**
   ```
   Course Details → ➕ Create Activity
   
   选项A - 手动创建:
   - 选择活动类型
   - 填写问题和选项
   - 设置截止日期
   
   选项B - AI生成:
   - 输入教学内容
   - AI自动生成问题
   - 预览并确认
   ```

5. **分享活动**
   ```
   Activity Details → 🔗 Copy Link
   分享给学生
   ```

6. **查看结果**
   ```
   Activity Details → 查看学生回答
   查看AI评估(Short Answer/Word Cloud)
   ```

#### 学生快速指南 (3分钟)

1. **注册课程**
   ```
   Student Dashboard → Browse Courses
   输入课程代码(教师提供)
   点击 Register
   ```

2. **参与活动**
   ```
   选项A - 点击分享链接
   选项B - My Activities → Start
   
   回答问题
   点击 Submit Answer
   ```

3. **查看AI反馈**
   ```
   提交后立即显示AI评估:
   - 分数
   - 详细反馈
   - 优点和改进建议
   ```

4. **查看排名**
   ```
   Leaderboard → 查看个人排名
   ```

### 高级功能

#### AI 生成活动最佳实践

**1. 准备高质量的输入内容**:
- ✅ 内容清晰,逻辑完整
- ✅ 包含关键概念和术语
- ✅ 长度适中(300-2000字)
- ❌ 避免过于简短或零碎

**2. 选择合适的文件格式**:
- PDF: 适合正式文档
- TXT: 适合纯文本内容
- DOCX: 适合格式化文档
- 文件大小控制在5MB以内

**3. Poll 生成技巧**:
- 教学内容应包含事实性知识
- 适合生成2-5个问题
- AI会自动标记正确答案

**4. Short Answer 生成技巧**:
- 输入应包含需要解释的概念
- AI会生成开放性问题
- 自动提取关键评分点

**示例输入**:
```
主题: Python 函数

函数是组织好的、可重复使用的代码块。在Python中,
使用def关键字定义函数。函数可以接收参数并返回值。
函数的优点包括:代码复用、模块化、易于维护。

示例:
def greet(name):
    return f"Hello, {name}!"

调用函数:
result = greet("Alice")  # 返回 "Hello, Alice!"
```

**AI 生成结果**:
```
Poll Questions:
1. 在Python中,使用什么关键字定义函数?
   A. function
   B. def ✅
   C. func
   D. define

2. 函数的主要优点不包括:
   A. 代码复用
   B. 模块化
   C. 运行更快 ✅
   D. 易于维护
```

#### 积分系统详解

**积分来源**:

| 活动类型 | 基础积分 | 额外积分 |
|---------|---------|---------|
| Poll | 10 | +5 (正确答案) |
| Short Answer | 基于AI评分 | 0-20 (90分以上+5) |
| Word Cloud | 10 | +5 (关键词质量高) |

**积分计算公式**:

**Poll**:
```
积分 = 10 (参与) + (答对 ? 5 : 0)
```

**Short Answer**:
```
积分 = (AI评分 / 100) × 20
例: 85分 → 17积分
```

**Word Cloud**:
```
积分 = 10 (基础) + AI质量评估 (0-10)
```

**徽章系统**:

| 徽章 | 获得条件 | 图标 |
|------|---------|------|
| First Response | 首次完成活动 | 🎯 |
| Perfect Score | 获得满分(Poll) | 🌟 |
| Speed Demon | 最快完成活动 | ⚡ |
| Active Learner | 完成10个活动 | 📚 |
| Top 10 | 进入前10名 | 🏆 |
| Top 3 | 进入前3名 | 🥇 |

#### 数据导出

**导出学生名单**:
```
Course Details → Export Students → CSV
包含: 学号, 姓名, 邮箱, 积分, 完成数
```

**导出活动结果**:
```
Activity Details → Export Data → CSV
包含: 学生信息, 答案, 得分, 提交时间
```

**导出排行榜**:
```
Leaderboard → Export → CSV
包含: 排名, 学生, 积分, 活动数, 徽章
```

---

## 常见问题

### 系统访问

**Q: 如何获取账号?**

A: 
- **教师**: 联系系统管理员创建账号
- **学生**: 由教师导入或使用课程代码自助注册

**Q: 忘记密码怎么办?**

A: 目前系统不支持自助重置密码,请联系管理员重置。

**Q: 可以更改用户名吗?**

A: 用户名创建后不可更改,但可以更新邮箱和机构信息。

### 课程管理

**Q: 课程代码重复怎么办?**

A: 课程代码必须唯一,如果提示重复,请使用其他代码,如添加学期后缀: CS101-Fall2025

**Q: 如何批量导入学生?**

A: 准备CSV文件,格式为: `student_id,name,email`,然后在课程详情页上传。

**Q: 学生可以退出课程吗?**

A: 目前不支持学生自助退课,需要教师在学生列表中操作。

**Q: 可以限制课程可见性吗?**

A: 所有活跃课程默认对学生可见,学生可以通过课程代码注册。

### 活动创建

**Q: AI 生成需要多长时间?**

A: 通常5-10秒,取决于内容长度和服务器负载。

**Q: AI 生成的内容可以修改吗?**

A: 预览阶段可以选择不同的生成结果,确认创建后不可修改。建议使用手动创建模式以获得完全控制。

**Q: 支持哪些文件格式?**

A: PDF, TXT, DOCX, 最大5MB。

**Q: 活动创建后可以编辑吗?**

A: 目前不支持编辑已创建的活动,建议创建前仔细检查。如需修改,删除后重新创建。

**Q: 可以设置活动的答案可见性吗?**

A: Poll 活动提交后立即显示正确答案。Short Answer 和 Word Cloud 的AI评估仅对学生本人和教师可见。

### 学生参与

**Q: 学生可以修改答案吗?**

A: 可以,学生可以重新提交答案。每次提交都会保存,教师可以看到所有提交记录。

**Q: Short Answer 的 AI 评估准确吗?**

A: AI 评估基于 GPT-4o-mini,准确率较高,但建议教师查看并可以手动调整。AI 提供参考意见,最终评分权在教师。

**Q: 过了截止日期还能提交吗?**

A: 不能。系统会在截止日期后自动禁止提交。

**Q: 积分如何计算?**

A: 不同活动类型有不同规则。Poll基于正确率,Short Answer基于AI评分,Word Cloud基于关键词质量。详见"积分系统详解"。

### 技术问题

**Q: 浏览器兼容性?**

A: 支持所有现代浏览器:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Q: 移动设备支持?**

A: 完全支持移动设备,界面自适应。建议使用横屏模式以获得更好体验。

**Q: 数据多久备份一次?**

A: MongoDB 数据每日自动备份。关键操作(创建/删除)实时记录日志。

**Q: 系统支持多少并发用户?**

A: 当前配置支持500+并发用户。如需更高并发,请联系管理员升级服务器。

### AI 功能

**Q: AI 生成的内容质量如何保证?**

A: 
- 使用 OpenAI GPT-4o-mini 模型
- 基于教学内容训练的提示词
- 生成后可预览,不满意可重新生成
- 教师可以选择手动创建以获得完全控制

**Q: AI 评估有偏见吗?**

A: AI 评估基于以下标准:
- 内容相关性
- 逻辑清晰度
- 关键概念覆盖
- 语言表达
教师应审查AI评估结果,必要时手动调整。

**Q: AI 评估支持中文吗?**

A: 完全支持中英文混合评估。

**Q: 可以关闭 AI 功能吗?**

A: 可以选择不使用AI生成,手动创建活动。AI评估是Short Answer和Word Cloud的默认功能,无法关闭。

---

## 联系支持

### 技术支持

**问题反馈**: 
- GitHub Issues: https://github.com/COMP5241-2526Sem1/groupproject-team_3/issues
- Email: support@learningsystem.edu

**文档更新**:
- 本文档持续更新
- 最新版本: v1.0.0
- 更新日期: 2025-11-13

### 开发团队

**项目仓库**: https://github.com/COMP5241-2526Sem1/groupproject-team_3

**技术栈**:
- Backend: Python + Flask
- Database: MongoDB
- AI: OpenAI GPT-4o-mini
- Frontend: HTML/CSS/JavaScript
- Deployment: Vercel

---

## 附录

### A. 快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl + / | 全局搜索 |
| Ctrl + N | 新建活动 |
| Ctrl + S | 保存(表单中) |
| Esc | 关闭模态框 |

### B. API 端点 (开发者)

系统主要 API 端点:

```
Authentication:
POST   /login              # 用户登录
GET    /logout             # 用户登出

Admin:
GET    /admin              # 管理员仪表盘
GET    /admin/users        # 用户管理页面
GET    /admin/api/users    # 获取用户列表
POST   /admin/api/users    # 创建用户
PUT    /admin/api/users/:id # 更新用户
DELETE /admin/api/users/:id # 删除用户

Teacher:
GET    /dashboard          # 教师仪表盘
POST   /course/create      # 创建课程
POST   /activity/create    # 创建活动
POST   /activity/ai-generate # AI生成活动

Student:
GET    /student/dashboard  # 学生仪表盘
POST   /student/register-course # 注册课程
POST   /activity/:id/submit # 提交答案
```

### C. 环境变量

```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27017/learning_activity_system

# OpenAI API
GITHUB_TOKEN=your_github_token_here

# Flask
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# Application
PORT=5000
DEBUG=True
```

### D. 数据库备份

**手动备份命令**:
```bash
mongodump --db learning_activity_system --out ./backup/$(date +%Y%m%d)
```

**恢复命令**:
```bash
mongorestore --db learning_activity_system ./backup/20251113
```

### E. 更新日志

**v1.0.0 (2025-11-13)**:
- ✅ 初始版本发布
- ✅ 管理员系统完整
- ✅ AI 功能集成
- ✅ 积分系统上线
- ✅ 移动端优化

**即将推出**:
- 📧 邮件通知系统
- 📱 移动应用
- 📊 高级数据分析
- 🎨 自定义主题
- 🌍 多语言支持

---

## 结语

感谢使用 Learning Activity Management System!

本系统旨在通过技术手段促进教育创新,提升教学效率和学习体验。我们持续改进系统功能,欢迎您的反馈和建议。

**祝教学愉快,学习进步!** 🎓

---

*文档版本: v1.0.0*  
*最后更新: 2025年11月13日*  
*维护团队: COMP5241 Team 3*
