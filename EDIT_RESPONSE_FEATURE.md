# 学生回答编辑功能 (Edit Response Feature)

## 功能概述

学生现在可以编辑和重新提交 **Short Answer** 和 **Word Cloud** 类型活动的回答。

### 支持的活动类型
- ✅ **Short Answer** - 可编辑
- ✅ **Word Cloud** - 可编辑  
- ❌ **Poll** - 不可编辑 (因为已经评分)

## 使用方法

### 编辑 Short Answer 回答

1. 学生完成 Short Answer 活动后，会看到自己的回答
2. 点击 **"✏️ Edit Answer"** 按钮
3. 文本框会显示原回答内容
4. 修改内容后点击 **"Update Answer"** 提交
5. 或点击 **"Cancel"** 取消编辑

### 编辑 Word Cloud 关键词

1. 学生完成 Word Cloud 活动后，会看到提交的关键词列表
2. 点击 **"✏️ Edit Keywords"** 按钮
3. 可以添加新关键词或删除现有关键词(点击 ×)
4. 保持 3-5 个关键词的限制
5. 点击 **"Update Keywords"** 提交更新
6. 或点击 **"Cancel"** 取消编辑

## 技术实现

### 后端实现 (Backend)

#### 1. 新增模型方法 `models/activity.py`
```python
@staticmethod
def update_response(activity_id, student_identifier, response_data):
    """更新学生已存在的回答"""
    # 通过 student_id 或 student_name 找到回答
    # 使用 MongoDB 数组位置更新: responses.{index}.{field}
    # 如果找不到回答，回退到 add_response()
```

#### 2. 修改提交路由 `routes/activity_routes.py`
```python
# 检测是否为更新操作
is_update = data.get('is_update', False)

# 根据活动类型决定更新或添加
if is_update and activity['type'] in ['short_answer', 'word_cloud']:
    success = Activity.update_response(activity_id, student_identifier, response_data)
else:
    success = Activity.add_response(activity_id, response_data)
```

### 前端实现 (Frontend)

#### 1. 编辑按钮 `templates/student/activity.html`
- 为已提交回答添加"Edit"按钮
- 按钮调用 `enableEdit(activityType)` 函数

#### 2. JavaScript 函数
- **enableEdit()** - 切换到编辑模式，显示表单
- **submitEdit()** - 提交更新的回答(包含 `is_update: true` 标志)
- **cancelEdit()** - 取消编辑，恢复原显示
- **addKeyword() / removeKeyword()** - Word Cloud 关键词管理
- **renderKeywords()** - 渲染关键词标签

## 数据库更新

使用 MongoDB 数组位置更新语法:
```python
{
    '$set': {
        'responses.0.text': 'new answer',
        'responses.0.submitted_at': datetime.utcnow()
    }
}
```

## 测试步骤

### 测试 Short Answer 编辑

1. 以学生身份登录
2. 进入一个 Short Answer 活动
3. 提交初始回答(例如: "Initial answer")
4. 查看回答显示
5. 点击 "Edit Answer" 按钮
6. 修改文本(例如: "Updated answer")
7. 点击 "Update Answer"
8. 确认页面刷新后显示新回答
9. 检查 MongoDB 中 `submitted_at` 时间戳已更新

### 测试 Word Cloud 编辑

1. 以学生身份登录
2. 进入一个 Word Cloud 活动
3. 添加 3-5 个关键词并提交
4. 查看关键词显示
5. 点击 "Edit Keywords" 按钮
6. 删除一个关键词(点击 ×)
7. 添加一个新关键词
8. 点击 "Update Keywords"
9. 确认页面刷新后显示更新后的关键词列表

### 测试取消编辑

1. 点击 "Edit Answer" 或 "Edit Keywords"
2. 修改内容
3. 点击 "Cancel" 按钮
4. 确认恢复到原显示状态
5. 确认编辑按钮重新出现

### 测试 Poll 不可编辑

1. 完成一个 Poll 活动
2. 确认没有 "Edit" 按钮显示
3. 确认回答显示为只读(已评分)

## 边界情况处理

- ✅ 回答不存在时回退到 `add_response()`
- ✅ 匿名学生使用 `student_name` 标识
- ✅ 已登录学生使用 `student_id` 标识
- ✅ Word Cloud 保持 3-5 关键词限制
- ✅ Short Answer 字数统计实时更新
- ✅ 取消编辑恢复原数据

## 文件修改清单

```
修改的文件:
├── models/activity.py (新增 update_response 方法)
├── routes/activity_routes.py (修改 submit_response 路由)
└── templates/student/activity.html (添加编辑 UI 和 JavaScript)
```

## 部署注意事项

1. 无需数据库迁移(使用现有 responses 数组)
2. 向后兼容现有回答数据
3. 功能对所有活动类型透明(Poll 自动禁用编辑)
4. 提交到 Vercel 前确保本地测试通过

## 下次改进建议

- [ ] 添加编辑历史记录(edit_history 数组)
- [ ] 显示"最后编辑于"时间戳
- [ ] 添加加载状态和成功提示动画
- [ ] 实现乐观 UI 更新(不刷新页面)
- [ ] 添加编辑次数限制(可选)
- [ ] 记录编辑操作日志

---

**功能状态**: ✅ 已完成并可测试  
**作者**: GitHub Copilot  
**日期**: 2024
