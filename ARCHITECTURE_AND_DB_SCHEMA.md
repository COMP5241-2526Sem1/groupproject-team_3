# Program Architecture & Database Schema / 程序架构与数据库结构

This document describes the high-level architecture of the project and the database schema in both English and Chinese (side-by-side). Use this as a quick reference for developers and testers.

本文件以中英文对照的方式介绍项目的高层架构与数据库结构，供开发和测试人员快速参考。

---

## Table of Contents / 目录

- Program Overview / 项目概述
- Application Architecture / 应用架构
  - Blueprints / 蓝图（模块路由）
  - Services / 服务层
  - Models / 数据模型
  - Templates & Static / 模板与静态资源
- Data Flow / 数据流
- Database Schema / 数据库结构
  - users collection / users 集合
  - courses collection / courses 集合
  - activities collection / activities 集合
  - students collection / students 集合
  - other collections / 其他集合
- How to read object examples / 对象示例说明
- Notes and best practices / 注意事项与最佳实践

---

## Program Overview / 项目概述

- English: This is a Flask-based learning activity system. It supports user roles (student, teacher, admin), course creation, activities (polls, short answers, word clouds), and tracking student responses and progress.

- 中文: 基于 Flask 的学习活动系统。支持多角色（学生、教师、管理员）、课程创建、活动（投票、简答、词云等）、以及学生答题与进度追踪。

---

## Application Architecture / 应用架构

### 1. Blueprints (routes) / 蓝图（路由模块）

- English: The app uses Flask Blueprints to organize routes by feature. Key blueprints include:
  - `auth_bp` (authentication routes)
  - `student_bp` (student-facing routes: dashboard, browse, course detail)
  - `course_bp` (course management routes for teachers/admin)
  - `activity_bp` (activity creation and viewing)

- 中文: 使用 Flask 蓝图按功能组织路由。主要蓝图包括：
  - `auth_bp`（身份验证相关路由）
  - `student_bp`（学生端路由：仪表盘、浏览、课程详情）
  - `course_bp`（教师/管理员的课程管理路由）
  - `activity_bp`（活动创建与查看）

Files: `routes/*.py` (e.g., `routes/student_routes.py`, `routes/course_routes.py`)

文件：位于 `routes/` 下的文件（如 `routes/student_routes.py`, `routes/course_routes.py`）

---

### 2. Services / 服务层

- English: Reusable services abstract database and external functionality:
  - `db_service.py` – thin wrapper around PyMongo operations
  - `auth_service.py` – registration, hashing, login helpers
  - `genai_service.py` – any generative AI integrations (if used)

- 中文: 可复用的服务层封装数据库和外部功能：
  - `db_service.py` – 封装 PyMongo 的数据库操作
  - `auth_service.py` – 注册、密码哈希、登录帮助函数
  - `genai_service.py` – 若使用则为生成式 AI 集成

Files: `services/*.py`

文件：位于 `services/` 目录

---

### 3. Models / 数据模型

- English: Models are plain Python modules that provide find/insert helpers and shape data for templates.
  - `models/user.py` – user structure, role, enrolled courses
  - `models/course.py` – course metadata and teacher reference
  - `models/activity.py` – activities, types, responses
  - `models/student.py` – enrollment records (per-course student entries)

- 中文: 模型为 Python 模块，提供查找/插入等数据库辅助函数并为模板准备数据。
  - `models/user.py` – 用户结构，角色，已选课程
  - `models/course.py` – 课程元数据与教师引用
  - `models/activity.py` – 活动，类型，回复
  - `models/student.py` – 学生选课记录（每门课程的学生条目）

Files: `models/*.py`

文件：位于 `models/` 目录

---

### 4. Templates & Static / 模板与静态资源

- English: Jinja2 templates in `templates/` render the UI. Static CSS/JS in `static/`.
- 中文: Jinja2 模板保存在 `templates/`，静态资源（CSS/JS）在 `static/`。

Key templates:
- `templates/student/dashboard.html` – student dashboard
- `templates/course_detail.html` – course detail for teacher
- `templates/student/course_detail.html` – student view of course

关键模板如上

---

## Data Flow / 数据流

- English:
  1. User logs in (session created).
  2. Student enrolls in course: `users.enrolled_courses` updated AND a `students` collection record is created.
  3. Activities are created under a course (stored in `activities` collection).
  4. When a student participates, a response object is added into the activity's `responses` array.
  5. Dashboard and course detail pages calculate completion by scanning `activities[].responses` for the student's `student_id`.

- 中文:
  1. 用户登录（创建会话）。
  2. 学生选课：更新 `users.enrolled_courses` 并在 `students` 集合中插入记录。
  3. 活动被添加到课程（存储在 `activities` 集合）。
  4. 学生参与活动时，在对应活动的 `responses` 数组中追加回复对象。
  5. 仪表盘与课程详情通过扫描 `activities[].responses` 中匹配 `student_id` 的回复来计算完成度。

---

## Database Schema / 数据库结构

Notes: The project uses MongoDB (PyMongo). Below are representative document structures.

注意：项目使用 MongoDB（通过 PyMongo）。下面为示例文档结构。

### 1. users collection / users 集合

English example:
```json
{
  "_id": ObjectId("..."),
  "username": "student_demo",
  "password_hash": "...",
  "email": "student@example.com",
  "role": "student", // or 'teacher', 'admin'
  "student_id": "S2024001", // application-level student id
  "institution": "Test University",
  "enrolled_courses": [ ObjectId("courseId1"), ObjectId("courseId2") ],
  "created_at": ISODate("2024-10-17T12:00:00Z")
}
```

中文说明：
- `_id`：MongoDB ObjectId
- `username`：用户名
- `password_hash`：哈希后的密码
- `role`：角色（student / teacher / admin）
- `student_id`：应用层的学生编号，用于在 `activities.responses` 中标识学生
- `enrolled_courses`：存储已选课程的 ObjectId 列表

---

### 2. courses collection / courses 集合

English example:
```json
{
  "_id": ObjectId("courseId1"),
  "code": "CS101",
  "name": "Introduction to Python Programming",
  "description": "...",
  "teacher_id": ObjectId("teacherUserId"),
  "created_at": ISODate("2024-10-17T12:00:00Z")
}
```

中文说明：课程文档包含课程代码、名称、描述与教师引用等。

---

### 3. activities collection / activities 集合

English example:
```json
{
  "_id": ObjectId("actId1"),
  "course_id": ObjectId("courseId1"),
  "title": "Python Basics Quiz",
  "type": "poll|short_answer|word_cloud",
  "created_at": ISODate("2024-10-17T12:10:00Z"),
  "responses": [
    {
      "student_id": "S2024001",
      "response": "...",
      "submitted_at": ISODate("2024-10-17T12:20:00Z")
    }
  ]
}
```

中文说明：活动文档包含所属课程、类型、以及学生回复数组。回复对象至少包含 `student_id` 与 `response`。

---

### 4. students collection / students 集合

English example:
```json
{
  "_id": ObjectId("stuRec1"),
  "student_id": "S2024001", // matches users.student_id
  "name": "student_demo",
  "email": "student@example.com",
  "course_id": ObjectId("courseId1"),
  "created_at": ISODate("2024-10-17T12:05:00Z")
}
```

中文说明：`students` 集合用于为教师快速查找某门课程的学生列表，存储每条选课记录及时间戳。

---

### 5. other collections / 其他集合

- sessions (optional) / 会话（可选）
- logs / 日志
- uploads (file metadata) / 上传文件的元数据

---

## How to read object examples / 如何阅读示例对象

- Fields in JSON examples use typical MongoDB types (ObjectId, ISODate). When you query via PyMongo, dates map to Python `datetime` objects.
- `student_id` is an application-level identifier (string) used throughout responses; do not confuse with MongoDB `_id`.

示例中使用了 MongoDB 类型（ObjectId、ISODate）。通过 PyMongo 查询时，日期类型会映射为 Python 的 `datetime` 对象。

---

## Notes and best practices / 注意事项与最佳实践

- Keep `student_id` consistent across `users` and `activities.responses`.
- When calculating progress, count responses in `activities.responses` for the student rather than relying solely on `users.enrolled_courses`.
- Consider adding indexes on `activities.course_id`, `students.course_id`, and `users.enrolled_courses` for performance.
- If performance becomes an issue, maintain a denormalized progress cache for each student-course pair.

- 保持 `student_id` 在 `users` 和 `activities.responses` 中一致。
- 计算进度时，应扫描 `activities.responses` 来判断学生是否完成活动，而非仅依赖 `users.enrolled_courses`。
- 建议在 `activities.course_id`、`students.course_id`、`users.enrolled_courses` 上添加索引以提高性能。
- 若性能成为瓶颈，可考虑为每个学生-课程对维护去范式化的进度缓存。

---

## Contact / 联系方式

If you need further clarifications, open an issue or message the project maintainers.

如需进一步说明，请在项目中打开 issue 或联系项目维护人员。
