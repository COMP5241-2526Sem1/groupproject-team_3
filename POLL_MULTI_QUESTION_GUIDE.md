# Poll 多题功能与答案评判系统使用指南

## 📋 功能概述

系统现在支持为 **Poll 活动生成 1-10 道题目**,并且每道题目都有**正确答案**和**详细解释**。学生提交答案后,系统会**自动评分**并显示**详细的答题反馈**。

---

## ✨ 新功能特性

### 1. 多题生成选项 (1-10 题)
- 教师可以选择生成 1-10 道 Poll 题目
- AI 会根据教学内容自动生成相关问题
- 每道题目都有 4 个选项 (A, B, C, D)

### 2. 正确答案与解释
- 每道题目都标明正确答案
- 提供详细的答案解释
- 帮助学生理解知识点

### 3. 自动评分系统
- 学生提交后立即显示得分
- 显示总分、正确题数和百分比
- 每道题显示对错状态

### 4. 详细反馈
- 显示学生选择的答案
- 对于错误答案,显示正确答案
- 每道题都有详细解释

---

## 🎓 使用步骤

### 教师端:创建多题 Poll 活动

#### 步骤 1: 选择 AI 辅助创建
1. 登录教师账号
2. 进入 **Create Activity** 页面
3. 选择 **🤖 AI-Assisted** 创建方式

#### 步骤 2: 配置活动参数
```
📝 填写表单:
├── Course: 选择课程
├── Activity Type: 选择 "📊 Poll"
├── Number of Questions: 输入题目数量 (1-10)
└── Teaching Content: 输入教学主题/关键词
```

**示例输入:**
```
Course: COMP5241 - Advanced Topics in IT
Activity Type: Poll
Number of Questions: 5
Teaching Content: TCP/IP protocol, network layers, OSI model
```

#### 步骤 3: 生成并预览
1. 点击 **🤖 Generate with AI** 按钮
2. 等待 AI 生成内容 (通常 5-10 秒)
3. 预览生成的题目:
   - 查看每道题的问题内容
   - 查看选项 (标记 ✅ 的是正确答案)
   - 查看答案解释

#### 步骤 4: 确认创建
- 如果满意,点击 **✅ Use This Activity**
- 如果不满意,点击 **🔄 Generate Again** 重新生成
- 活动创建后会生成唯一链接供学生访问

---

### 学生端:参与多题 Poll 活动

#### 步骤 1: 访问活动链接
- 点击教师分享的活动链接
- 或从课程页面进入活动

#### 步骤 2: 填写个人信息 (可选)
```
Student ID: 输入学号 (可选)
Name: 输入姓名 (可选)
```

#### 步骤 3: 回答所有问题
- 每道题选择一个答案 (单选)
- 必须回答所有问题才能提交
- 系统会提示未回答的题目

#### 步骤 4: 提交并查看结果
提交后立即显示:
```
🎉 Quiz Results

5 / 5
Score: 100%

Detailed Results:
✅ Question 1 - Correct
   Your answer: A
   Explanation: ...

❌ Question 2 - Incorrect  
   Your answer: B
   Correct answer: C
   Explanation: ...
```

---

## 📊 评分系统说明

### 评分标准
- **每道题 1 分**
- **总分 = 正确题数**
- **百分比 = (正确题数 / 总题数) × 100%**

### 结果显示
根据得分显示不同图标:
- **≥ 70%**: 🎉 (优秀)
- **50-69%**: 👍 (良好)
- **< 50%**: 📚 (需要努力)

### 详细反馈
每道题显示:
- ✅ **正确**: 绿色背景 + 答案解释
- ❌ **错误**: 红色背景 + 正确答案 + 答案解释

---

## 💡 使用技巧

### 教师技巧

1. **合理设置题目数量**
   - 快速测验: 3-5 题
   - 课堂练习: 5-8 题
   - 章节测试: 8-10 题

2. **优化教学内容输入**
   ```
   好的输入示例:
   "TCP three-way handshake, SYN, ACK flags, 
    connection establishment process"
   
   不好的输入:
   "networking" (太笼统)
   ```

3. **预览检查**
   - 确认题目难度合适
   - 检查答案是否准确
   - 查看解释是否清晰

4. **重新生成策略**
   - 如果题目重复,点击 "Generate Again"
   - 如果难度不合适,调整教学内容描述
   - 可以多次生成直到满意

### 学生技巧

1. **仔细阅读每道题**
   - 不要急于选择
   - 注意关键词和细节

2. **检查再提交**
   - 确保所有题目都已回答
   - 提交前再次确认答案

3. **学习反馈内容**
   - 仔细阅读答案解释
   - 理解错误原因
   - 记录知识盲点

---

## 🔧 技术实现细节

### AI 生成格式
```json
{
  "title": "TCP/IP Protocol Quiz",
  "questions": [
    {
      "question": "What is the first step in TCP three-way handshake?",
      "options": [
        {"label": "A", "text": "Client sends SYN"},
        {"label": "B", "text": "Server sends ACK"},
        {"label": "C", "text": "Client sends FIN"},
        {"label": "D", "text": "Server sends RST"}
      ],
      "correct_answer": "A",
      "explanation": "The client initiates connection by sending SYN packet"
    }
  ]
}
```

### 数据存储结构
```javascript
// 活动内容
{
  type: 'poll',
  content: {
    questions: [
      {
        question: "...",
        options: [...],
        correct_answer: "A",
        explanation: "..."
      }
    ]
  }
}

// 学生回答
{
  student_id: "123456",
  student_name: "John Doe",
  answers: [
    {
      question_index: 0,
      student_answer: "A",
      correct_answer: "A",
      is_correct: true,
      explanation: "..."
    }
  ],
  score: 5,
  total: 5,
  percentage: 100.0
}
```

---

## 🎯 最佳实践

### 创建高质量 Poll 的建议

1. **明确的教学内容**
   ```
   ✅ 好例子:
   "OSI model layers, Layer 3 (Network Layer), 
    IP addressing, routing protocols"
   
   ❌ 避免:
   "computer stuff"
   ```

2. **合适的题目数量**
   - 课前预习: 3-5 题
   - 课堂互动: 5-7 题
   - 课后复习: 7-10 题

3. **题目类型多样化**
   - 概念理解题
   - 应用分析题
   - 场景判断题

4. **及时查看统计**
   - 查看学生答题率
   - 分析错误率高的题目
   - 调整教学重点

---

## 🐛 故障排除

### 常见问题

#### Q1: AI 生成失败怎么办?
**原因**: 
- API 密钥过期
- 网络连接问题
- 教学内容太短或太笼统

**解决方法**:
1. 检查 Vercel 环境变量 `OPENAI_API_KEY`
2. 详细描述教学内容 (至少 20 字)
3. 稍后重试

#### Q2: 学生看不到评分结果?
**原因**:
- 旧版本活动 (创建时没有正确答案)
- 浏览器缓存问题

**解决方法**:
1. 重新创建活动 (使用新版本)
2. 清除浏览器缓存
3. 使用隐身模式测试

#### Q3: 题目数量显示不对?
**原因**:
- 选择了非 Poll 类型
- num_questions 参数未传递

**解决方法**:
1. 确保选择 "📊 Poll" 类型
2. 刷新页面重试
3. 检查浏览器控制台错误

#### Q4: 答案解释显示不完整?
**原因**:
- AI 生成的解释过长
- 数据库字段限制

**解决方法**:
1. 重新生成活动
2. 在预览时检查解释长度
3. 如果太长,可以手动编辑数据库

---

## 📈 数据分析

### 教师可以查看的统计数据

1. **参与率**
   - 已回答学生数 / 课程学生数

2. **平均分**
   - 所有学生得分的平均值

3. **题目难度分析**
   - 每道题的正确率
   - 识别难点题目

4. **学生表现**
   - 个人得分
   - 答题时间
   - 错误分布

---

## 🚀 未来计划

### 即将推出的功能

- [ ] 自定义题目难度级别
- [ ] 题库管理 (保存常用题目)
- [ ] 随机题目顺序
- [ ] 限时答题
- [ ] 多次尝试机会
- [ ] 成绩排行榜
- [ ] 导出成绩报表

---

## 📞 获取帮助

如果遇到问题:
1. 查看本指南的故障排除部分
2. 检查 Vercel 部署日志
3. 查看浏览器控制台错误信息
4. 联系系统管理员

---

**文档版本**: 1.0  
**最后更新**: 2025-10-28  
**适用版本**: v2.0+  

🎉 **Happy Teaching & Learning!**
