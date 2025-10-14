# 🎯 快速测试参考卡

## 🔑 测试账号

### 👨‍🏫 教师账号
```
用户名: teacher_demo
密码: teacher123
预期: 看到 "New Course" 和 "New Activity" 按钮
```

### 👨‍🎓 学生账号  
```
用户名: student_demo
密码: student123
预期: 看到学生专属界面，无创建功能
```

### 👤 管理员账号
```
用户名: admin
密码: admin123
预期: 看到管理员仪表盘
```

---

## 📊 数据库内容概览

### 课程 (5门)
- CS101: Introduction to Python Programming (3活动)
- CS102: Data Structures and Algorithms (3活动)
- CS201: Web Development with Flask (2活动)
- CS301: Machine Learning Fundamentals (3活动)
- CS202: Database Management Systems (2活动)

### 学生注册
- student_demo: 已注册 CS101, CS102, CS201
- alice_wang: 已注册 CS101, CS102, CS201  
- bob_chen: 已注册 CS101, CS102, CS201

### 活动总数: 13个
- 📊 Poll: 5个
- ✍️ Short Answer: 5个
- ☁️ Word Cloud: 3个

---

## ✅ 学生界面检查清单

登录 `student_demo` 后应该看到：

### 导航栏
- [ ] 🏠 My Dashboard
- [ ] 📚 My Courses
- [ ] 🔍 Browse Courses
- [ ] ✏️ My Activities
- [ ] 🏆 Leaderboard
- [ ] ❌ **没有** "New Course"
- [ ] ❌ **没有** "New Activity"

### 仪表盘内容
- [ ] 欢迎信息: "Welcome, student_demo!"
- [ ] 学号显示: "Student ID: S2024001"
- [ ] 4个彩色统计卡片（渐变色背景）
- [ ] 快速操作按钮 (3个)
- [ ] 近期活动表格
- [ ] 已注册课程卡片 (3个)
- [ ] ❌ **没有** "Create Course" 按钮

### 功能测试
- [ ] My Courses 显示3门课程
- [ ] Browse Courses 显示2门未注册课程
- [ ] My Activities 显示8个活动
- [ ] 可以点击 "Participate" 参与活动
- [ ] 可以注册新课程 (Enroll Now)

---

## ✅ 教师界面检查清单

登录 `teacher_demo` 后应该看到：

### 导航栏
- [ ] 📊 Dashboard
- [ ] ➕ New Course
- [ ] 📝 New Activity

### 仪表盘内容
- [ ] 标题: "Teacher Dashboard"
- [ ] ➕ New Course 按钮
- [ ] 📝 New Activity 按钮
- [ ] My Courses 部分显示5门课程
- [ ] 每门课程有 [Edit] [Delete] 按钮

---

## 🐛 常见问题

### Q: 学生登录后还是显示 "Teacher Dashboard"?
**A**: 
1. 完全退出登录
2. 清除浏览器缓存 (Ctrl+Shift+Delete)
3. 重新登录

### Q: 点击功能显示 ERROR?
**A**: 
1. 检查数据库连接
2. 确认Flask应用正在运行
3. 查看浏览器控制台错误 (F12)

### Q: My Courses 为空?
**A**: 
1. 数据已经添加，student_demo应该有3门课程
2. 如果为空，运行: `.\Project3\Scripts\python.exe seed_database.py`

---

## 🚀 重新运行种子脚本

如果需要重新填充数据：

```powershell
# 停止应用
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 运行种子脚本
.\Project3\Scripts\python.exe seed_database.py

# 重启应用
.\Project3\Scripts\python.exe app.py
```

---

## 📱 访问地址

**主页**: http://localhost:5000
**登录**: http://localhost:5000/login

---

**测试愉快！** ✨
