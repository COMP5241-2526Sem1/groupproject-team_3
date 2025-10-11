# 🧪 学生功能测试指南

## 快速测试步骤

### 1️⃣ 登录学生账号
```
用户名: student_demo
密码: student123
```

### 2️⃣ 测试 Dashboard (http://localhost:5000/student/dashboard)
**预期显示**:
- ✅ 4个统计卡片:
  * 📚 Enrolled Courses: 3
  * 📝 Total Activities: 8
  * ✅ Completed: X (根据你的完成情况)
  * 📊 Completion Rate: X%
  
- ✅ 3个快速操作按钮:
  * Browse Courses
  * View My Activities
  * View Leaderboard
  
- ✅ Recent Activities 表格:
  * 显示最近5个活动
  * 课程名称、活动标题、类型、状态

### 3️⃣ 测试 My Courses (http://localhost:5000/student/my-courses)
**预期显示**:
- ✅ 3门已注册课程:
  1. CS101 - Introduction to Python Programming
     * 进度条显示完成百分比
     * 活动数: 3
  2. CS102 - Data Structures and Algorithms
     * 进度条显示完成百分比
     * 活动数: 3
  3. CS201 - Web Development with Flask
     * 进度条显示完成百分比
     * 活动数: 2

### 4️⃣ 测试 Browse Courses (http://localhost:5000/student/browse-courses)
**预期显示**:
- ✅ 3门可用课程(未注册):
  * CS202 - Database Management Systems
  * CS301 - Machine Learning Fundamentals
  * CS001 - IT course1
- ✅ 每门课程显示:
  * 课程代码和名称
  * 描述
  * 教师名称
  * 活动数量
  * "Enroll" 按钮

### 5️⃣ 测试 My Activities (http://localhost:5000/student/my-activities)
**预期显示**:
- ✅ 8个活动列表:
  * 3个来自 CS101
  * 3个来自 CS102
  * 2个来自 CS201
- ✅ 每个活动显示:
  * 课程代码
  * 活动标题
  * 活动类型(Poll/Short Answer/Word Cloud)
  * 完成状态(Completed/Pending)
  * "View" 按钮

### 6️⃣ 测试 Leaderboard (http://localhost:5000/student/leaderboard)
**预期显示**:
- ✅ "Coming Soon" 提示(功能待实现)

## 🔍 故障排查

### 如果看到 ERROR 页面:
1. **检查应用是否运行**:
   ```powershell
   Get-Process | Where-Object {$_.Path -like "*python*"}
   ```

2. **重启应用**:
   ```powershell
   .\Project3\Scripts\python.exe app.py
   ```

3. **检查数据库连接**:
   - 确保 MongoDB 连接字符串正确
   - 确保网络连接正常

4. **查看应用日志**:
   - 终端会显示详细的错误信息
   - 检查是否有 `ERROR` 或 `Traceback` 信息

### 如果数据不显示:
1. **运行数据库seeding脚本**:
   ```powershell
   .\Project3\Scripts\python.exe seed_database.py
   ```

2. **验证数据**:
   ```powershell
   .\Project3\Scripts\python.exe check_student_data.py
   ```

## 📱 测试其他学生账号

### Alice Wang
```
用户名: alice_wang
密码: alice123
学号: S2024002
```

### Bob Chen
```
用户名: bob_chen
密码: bob123
学号: S2024003
```

## ✅ 验证清单

- [ ] Dashboard 正常显示统计数据
- [ ] My Courses 显示3门已注册课程
- [ ] Browse Courses 显示3门可用课程
- [ ] My Activities 显示8个活动
- [ ] 课程进度条正确显示百分比
- [ ] 活动完成状态正确(Completed/Pending)
- [ ] 导航菜单功能正常
- [ ] 页面加载无 ERROR 提示
- [ ] 样式显示正常(渐变卡片、动画效果)

## 🎯 下一步功能测试

1. **测试课程注册**:
   - Browse Courses → 点击 "Enroll" 按钮
   - 验证课程出现在 My Courses 中

2. **测试活动参与**:
   - My Activities → 点击 "View" 按钮
   - 提交回答
   - 验证状态变为 "Completed"

3. **测试响应式设计**:
   - 缩小浏览器窗口
   - 验证移动端布局

---
**测试日期**: 2025-10-12  
**测试版本**: v1.1 (修复 ObjectId 问题)  
**测试状态**: ✅ Ready
