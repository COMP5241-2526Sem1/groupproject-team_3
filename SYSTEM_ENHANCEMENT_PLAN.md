# 🚀 学习活动系统完善方案

## 📋 核心需求对照表

基于您提供的核心需求，以下是当前系统状态和需要完善的功能：

| 需求 | 当前状态 | 需要完善 | 优先级 |
|------|---------|---------|--------|
| 1. 多种学习活动（投票、小测验、词云、简答题、小游戏） | ✅ 投票、词云、简答题 | ⚠️ 小测验、小游戏 | 🔴 高 |
| 2. 教师创建课程并导入学生信息（与学生ID关联） | ✅ 创建课程、学生注册 | ⚠️ CSV批量导入学生 | 🔴 高 |
| 3. GenAI集成 - 创建学习活动 | ✅ AI生成活动内容 | ⚠️ 教师审核优化界面 | 🟡 中 |
| 4. GenAI集成 - 答案自动分组 | ✅ 相似答案分组 | ✅ 已实现 | ✅ 完成 |
| 5. 排行榜功能 | ❌ 未实现 | ⚠️ 学生积分、排行榜 | 🔴 高 |
| 6. 数据仪表盘和报告 | 🟡 基础仪表盘 | ⚠️ 数据可视化、报告导出 | 🟡 中 |
| 7. 管理员功能及数据仪表盘 | ✅ 管理员功能 | ⚠️ 完善数据统计 | 🟡 中 |
| 8. 响应式UI设计（移动设备支持） | ❌ 未实现 | ⚠️ 响应式CSS、移动优化 | 🔴 高 |

---

## 🎯 第一阶段：核心功能补全（优先级：🔴 高）

### 1. 小测验（Quiz）功能模块

#### 1.1 数据模型扩展

**文件**: `models/activity.py`

```python
# 添加新的活动类型
TYPE_QUIZ = 'quiz'

# Quiz 内容结构
quiz_content = {
    'questions': [
        {
            'question': '问题文本',
            'type': 'multiple_choice',  # multiple_choice, true_false, fill_blank
            'options': ['选项A', '选项B', '选项C', '选项D'],
            'correct_answer': '选项A',
            'points': 10,  # 分值
            'time_limit': 60  # 答题时间限制（秒）
        }
    ],
    'total_points': 100,
    'passing_score': 60,
    'time_limit': 600,  # 总时间限制（秒）
    'show_results': True,  # 是否立即显示结果
    'allow_review': True  # 是否允许答题后查看
}
```

#### 1.2 Quiz响应模型

**新增文件**: `models/quiz_response.py`

```python
class QuizResponse:
    """学生测验回答记录"""
    
    COLLECTION_NAME = 'quiz_responses'
    
    def __init__(self, activity_id, student_id, answers):
        self.activity_id = activity_id
        self.student_id = student_id
        self.answers = answers  # [{'question_id': 1, 'answer': 'A', 'is_correct': True}]
        self.score = 0
        self.total_points = 0
        self.percentage = 0
        self.time_taken = 0  # 用时（秒）
        self.submitted_at = datetime.utcnow()
    
    def calculate_score(self):
        """自动计算得分"""
        pass
    
    def get_leaderboard_position(self):
        """获取排名"""
        pass
```

#### 1.3 路由和视图

**文件**: `routes/activity_routes.py`

```python
@activity_bp.route('/quiz/<activity_id>', methods=['GET', 'POST'])
def quiz(activity_id):
    """小测验页面"""
    pass

@activity_bp.route('/quiz/<activity_id>/submit', methods=['POST'])
def submit_quiz(activity_id):
    """提交小测验答案"""
    pass

@activity_bp.route('/quiz/<activity_id>/results/<student_id>')
def quiz_results(activity_id, student_id):
    """显示测验结果"""
    pass
```

#### 1.4 前端模板

**新增文件**: 
- `templates/quiz.html` - 测验答题页面
- `templates/quiz_results.html` - 测验结果页面
- `templates/create_quiz.html` - 创建测验页面

---

### 2. 小游戏（Mini-Games）功能模块

#### 2.1 游戏类型设计

支持以下几种教育小游戏：

1. **单词匹配（Word Matching）**
   - 拖拽单词与定义进行匹配
   - 适用于：术语学习、外语学习

2. **排序游戏（Sequencing）**
   - 将打乱的步骤/事件按正确顺序排列
   - 适用于：流程学习、历史事件

3. **填空挑战（Fill in the Blanks）**
   - 在文本中快速填入正确词汇
   - 适用于：语法、公式、概念

4. **快问快答（Quick Quiz）**
   - 限时抢答，计分制
   - 适用于：知识点复习

#### 2.2 数据模型

**文件**: `models/activity.py`

```python
TYPE_GAME = 'game'

game_content = {
    'game_type': 'word_matching',  # word_matching, sequencing, fill_blanks, quick_quiz
    'title': '游戏标题',
    'instructions': '游戏说明',
    'items': [
        {'id': 1, 'term': 'HTTP', 'definition': '超文本传输协议'},
        {'id': 2, 'term': 'TCP', 'definition': '传输控制协议'}
    ],
    'time_limit': 120,
    'points_per_correct': 10,
    'penalty_per_wrong': -5
}
```

#### 2.3 前端实现

**新增文件**:
- `templates/games/word_matching.html`
- `templates/games/sequencing.html`
- `templates/games/fill_blanks.html`
- `static/js/game_engine.js` - 游戏逻辑引擎

---

### 3. CSV批量导入学生功能

#### 3.1 导入服务

**新增文件**: `services/import_service.py`

```python
import pandas as pd
import csv
from models.user import User
from services.auth_service import auth_service

class ImportService:
    """批量导入学生信息服务"""
    
    @staticmethod
    def import_students_from_csv(file_path, course_id=None):
        """
        从CSV文件导入学生
        
        CSV格式:
        student_id, username, email, full_name, institution
        S2024001, john_doe, john@polyu.edu.hk, John Doe, COMP
        
        Returns:
            dict: {
                'success': True/False,
                'imported': 10,
                'failed': 2,
                'errors': []
            }
        """
        try:
            df = pd.read_csv(file_path)
            results = {
                'success': True,
                'imported': 0,
                'failed': 0,
                'errors': []
            }
            
            for index, row in df.iterrows():
                try:
                    # 生成默认密码（可以是学号或统一密码）
                    default_password = row['student_id']
                    
                    result = auth_service.register_user(
                        username=row['username'],
                        password=default_password,
                        email=row['email'],
                        role='student',
                        institution=row.get('institution', 'PolyU'),
                        student_id=row['student_id'],
                        full_name=row.get('full_name', '')
                    )
                    
                    if result['success']:
                        results['imported'] += 1
                        
                        # 如果指定了课程ID，自动注册学生到课程
                        if course_id:
                            user = User.find_by_username(row['username'])
                            user.enroll_course(course_id)
                    else:
                        results['failed'] += 1
                        results['errors'].append({
                            'row': index + 2,
                            'student_id': row['student_id'],
                            'error': result['message']
                        })
                        
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append({
                        'row': index + 2,
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def generate_sample_csv():
        """生成CSV模板文件"""
        sample_data = [
            ['student_id', 'username', 'email', 'full_name', 'institution'],
            ['S2024001', 'john_doe', 'john.doe@polyu.edu.hk', 'John Doe', 'COMP'],
            ['S2024002', 'jane_smith', 'jane.smith@polyu.edu.hk', 'Jane Smith', 'COMP'],
            ['S2024003', 'bob_wang', 'bob.wang@polyu.edu.hk', 'Bob Wang', 'EIE']
        ]
        return sample_data
```

#### 3.2 路由

**文件**: `routes/course_routes.py`

```python
@course_bp.route('/course/<course_id>/import-students', methods=['GET', 'POST'])
@teacher_required
def import_students(course_id):
    """批量导入学生"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.csv'):
            # 保存临时文件
            temp_path = os.path.join('temp', file.filename)
            file.save(temp_path)
            
            # 导入学生
            result = ImportService.import_students_from_csv(temp_path, course_id)
            
            # 删除临时文件
            os.remove(temp_path)
            
            return jsonify(result)
    
    return render_template('import_students.html', course_id=course_id)

@course_bp.route('/download-student-template')
def download_template():
    """下载学生导入模板"""
    sample_data = ImportService.generate_sample_csv()
    # 生成CSV响应
    pass
```

#### 3.3 前端页面

**新增文件**: `templates/import_students.html`

```html
<div class="import-container">
    <h2>批量导入学生</h2>
    
    <div class="instructions">
        <h3>📋 导入步骤</h3>
        <ol>
            <li>下载 <a href="{{ url_for('course.download_template') }}">CSV模板文件</a></li>
            <li>填写学生信息（学号、用户名、邮箱等）</li>
            <li>上传填好的CSV文件</li>
            <li>系统将自动创建学生账号并注册到课程</li>
        </ol>
    </div>
    
    <form id="import-form" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required>
        <button type="submit">开始导入</button>
    </form>
    
    <div id="import-results" style="display:none;">
        <h3>导入结果</h3>
        <p>成功: <span id="success-count"></span></p>
        <p>失败: <span id="fail-count"></span></p>
        <div id="error-list"></div>
    </div>
</div>
```

---

### 4. 排行榜（Leaderboard）系统

#### 4.1 积分系统设计

**新增文件**: `models/points.py`

```python
class PointsSystem:
    """学生积分系统"""
    
    COLLECTION_NAME = 'student_points'
    
    # 积分规则
    POINTS_RULES = {
        'activity_complete': 10,      # 完成活动
        'quiz_pass': 50,              # 测验及格
        'quiz_perfect': 100,          # 测验满分
        'quick_answer': 5,            # 快速回答
        'helpful_answer': 20,         # 有价值的回答
        'participation': 5,           # 参与度
        'streak_bonus': 10            # 连续参与奖励
    }
    
    @staticmethod
    def award_points(student_id, course_id, activity_id, points, reason):
        """奖励积分"""
        pass
    
    @staticmethod
    def get_student_points(student_id, course_id=None):
        """获取学生积分"""
        pass
    
    @staticmethod
    def get_leaderboard(course_id, limit=10, time_range='all'):
        """
        获取排行榜
        
        Args:
            course_id: 课程ID（None为全局排行榜）
            limit: 显示人数
            time_range: 时间范围（all, week, month）
        """
        pass
```

#### 4.2 排行榜类型

1. **课程排行榜** - 单个课程内的学生排名
2. **全局排行榜** - 系统内所有学生排名
3. **活动排行榜** - 特定活动的排名（如Quiz得分）
4. **周榜/月榜** - 时间段内的活跃度排名

#### 4.3 路由

**新增文件**: `routes/leaderboard_routes.py`

```python
from flask import Blueprint, render_template
from models.points import PointsSystem

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/leaderboard/course/<course_id>')
def course_leaderboard(course_id):
    """课程排行榜"""
    rankings = PointsSystem.get_leaderboard(course_id, limit=50)
    return render_template('leaderboard.html', rankings=rankings, type='course')

@leaderboard_bp.route('/leaderboard/global')
def global_leaderboard():
    """全局排行榜"""
    rankings = PointsSystem.get_leaderboard(None, limit=100)
    return render_template('leaderboard.html', rankings=rankings, type='global')

@leaderboard_bp.route('/leaderboard/activity/<activity_id>')
def activity_leaderboard(activity_id):
    """活动排行榜（Quiz）"""
    pass
```

#### 4.4 前端页面

**新增文件**: `templates/leaderboard.html`

```html
<div class="leaderboard-container">
    <h1>🏆 排行榜</h1>
    
    <div class="tabs">
        <button class="tab active" data-range="week">本周</button>
        <button class="tab" data-range="month">本月</button>
        <button class="tab" data-range="all">全部</button>
    </div>
    
    <table class="leaderboard-table">
        <thead>
            <tr>
                <th>排名</th>
                <th>学生</th>
                <th>学号</th>
                <th>积分</th>
                <th>完成活动</th>
                <th>徽章</th>
            </tr>
        </thead>
        <tbody id="rankings">
            {% for rank in rankings %}
            <tr class="{% if loop.index <= 3 %}top-three{% endif %}">
                <td class="rank">
                    {% if loop.index == 1 %}🥇
                    {% elif loop.index == 2 %}🥈
                    {% elif loop.index == 3 %}🥉
                    {% else %}{{ loop.index }}
                    {% endif %}
                </td>
                <td>{{ rank.student_name }}</td>
                <td>{{ rank.student_id }}</td>
                <td class="points">{{ rank.total_points }}</td>
                <td>{{ rank.activities_completed }}</td>
                <td class="badges">
                    {% for badge in rank.badges %}
                    <span class="badge">{{ badge }}</span>
                    {% endfor %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

---

### 5. 响应式UI设计（移动设备支持）

#### 5.1 响应式CSS框架

**新增文件**: `static/css/responsive.css`

```css
/* 移动优先设计 */

/* 基础样式 - 移动设备（<768px） */
.container {
    width: 100%;
    padding: 15px;
}

.card {
    margin-bottom: 15px;
}

/* 平板设备（768px - 1024px） */
@media (min-width: 768px) {
    .container {
        max-width: 720px;
        margin: 0 auto;
    }
    
    .grid-2 {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
}

/* 桌面设备（>1024px） */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
    }
    
    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
    }
}

/* 移动导航菜单 */
@media (max-width: 768px) {
    .nav-menu {
        display: none;
        position: fixed;
        top: 60px;
        left: 0;
        width: 100%;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .nav-menu.active {
        display: block;
    }
    
    .hamburger {
        display: block;
    }
}

/* 触摸友好的按钮尺寸 */
@media (max-width: 768px) {
    button, .btn, a.btn {
        min-height: 44px;  /* iOS推荐触摸目标大小 */
        padding: 12px 20px;
        font-size: 16px;
    }
    
    input, textarea, select {
        font-size: 16px;  /* 防止iOS自动缩放 */
    }
}

/* 横屏模式优化 */
@media (max-width: 768px) and (orientation: landscape) {
    .header {
        height: 50px;
    }
}
```

#### 5.2 移动端优化页面

需要优化的关键页面：
1. ✅ 登录/注册页面
2. ✅ 仪表盘（Dashboard）
3. ✅ 课程列表
4. ✅ 活动参与页面
5. ✅ 排行榜
6. ✅ Quiz答题页面

#### 5.3 移动端JavaScript优化

**新增文件**: `static/js/mobile.js`

```javascript
// 检测设备类型
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

// 汉堡菜单切换
document.querySelector('.hamburger')?.addEventListener('click', () => {
    document.querySelector('.nav-menu').classList.toggle('active');
});

// 触摸滑动支持
if (isMobile) {
    // 添加触摸事件处理
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    document.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        if (touchEndX < touchStartX - 50) {
            // 向左滑动
        }
        if (touchEndX > touchStartX + 50) {
            // 向右滑动
        }
    }
}
```

---

## 📊 第二阶段：数据可视化增强（优先级：🟡 中）

### 1. 增强型教师仪表盘

#### 1.1 数据统计模块

**新增文件**: `services/analytics_service.py`

```python
class AnalyticsService:
    """数据分析服务"""
    
    @staticmethod
    def get_teacher_dashboard_stats(teacher_id):
        """
        获取教师仪表盘统计数据
        
        Returns:
            dict: {
                'total_courses': 5,
                'total_activities': 23,
                'total_students': 156,
                'active_students': 142,
                'avg_participation_rate': 0.87,
                'recent_activities': [...],
                'popular_courses': [...],
                'student_engagement': {...}
            }
        """
        pass
    
    @staticmethod
    def get_course_analytics(course_id):
        """
        课程详细分析
        
        Returns:
            dict: {
                'enrollment_trend': [...],  # 注册趋势
                'activity_completion_rate': {...},
                'student_performance': [...],
                'engagement_heatmap': [...],  # 活跃度热图
                'top_performers': [...]
            }
        """
        pass
    
    @staticmethod
    def get_activity_analytics(activity_id):
        """
        活动详细分析
        
        Returns:
            dict: {
                'total_responses': 45,
                'completion_rate': 0.85,
                'avg_score': 78.5,
                'time_distribution': [...],
                'answer_distribution': {...},
                'word_cloud_data': [...]
            }
        """
        pass
```

#### 1.2 可视化图表

使用 **Chart.js** 或 **ECharts** 实现数据可视化：

1. **折线图** - 学生参与度趋势
2. **柱状图** - 各活动完成率对比
3. **饼图** - 答案分布
4. **热力图** - 学生活跃时间分布
5. **词云图** - 学生回答关键词（已实现）

#### 1.3 报告导出功能

**路由**: `routes/report_routes.py`

```python
@report_bp.route('/export/course/<course_id>/pdf')
def export_course_report_pdf(course_id):
    """导出课程报告（PDF）"""
    pass

@report_bp.route('/export/course/<course_id>/excel')
def export_course_report_excel(course_id):
    """导出课程数据（Excel）"""
    # 使用 pandas 生成 Excel
    df = pd.DataFrame(course_data)
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    return send_file(excel_buffer, as_attachment=True, 
                     download_name=f'course_{course_id}_report.xlsx')
```

---

### 2. 学生数据仪表盘

#### 2.1 个人学习分析

**新增页面**: `templates/student/analytics.html`

显示内容：
- 📊 学习进度图表
- 🏆 获得的积分和徽章
- 📈 参与度曲线
- ✅ 完成的活动列表
- 🎯 学习目标达成情况
- 📝 各科目表现雷达图

#### 2.2 学习建议

使用AI生成个性化学习建议：

```python
def generate_learning_suggestions(student_id):
    """
    基于学生数据生成学习建议
    """
    student_data = get_student_analytics(student_id)
    
    prompt = f"""
    基于以下学生学习数据，生成3-5条个性化学习建议：
    
    - 完成活动数: {student_data['completed_activities']}
    - 平均得分: {student_data['avg_score']}
    - 薄弱科目: {student_data['weak_subjects']}
    - 学习时间分布: {student_data['time_distribution']}
    
    请提供具体、可操作的建议。
    """
    
    response = genai_service.client.chat.completions.create(
        model=genai_service.model,
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response.choices[0].message.content
```

---

### 3. 管理员数据仪表盘增强

#### 3.1 系统级统计

**文件**: `routes/admin_routes.py`

```python
@admin_bp.route('/admin/analytics')
@admin_required
def analytics():
    """系统分析页面"""
    stats = {
        'total_users': User.count_all(),
        'total_teachers': User.count_by_role('teacher'),
        'total_students': User.count_by_role('student'),
        'total_courses': Course.count_all(),
        'total_activities': Activity.count_all(),
        'active_users_today': get_active_users_count('today'),
        'active_users_week': get_active_users_count('week'),
        'system_health': check_system_health()
    }
    return render_template('admin/analytics.html', stats=stats)
```

#### 3.2 管理员功能

- 👥 用户管理（查看、编辑、删除、禁用）
- 📚 课程审核和管理
- 🔔 系统通知发布
- 📊 使用情况监控
- 🔒 权限管理
- 🗃️ 数据备份和恢复
- 📈 系统性能监控

---

## 🎨 第三阶段：用户体验优化（优先级：🟡 中）

### 1. AI功能增强

#### 1.1 教师审核AI生成内容的界面

**新增页面**: `templates/review_ai_activity.html`

```html
<div class="ai-review-container">
    <h2>📝 审核AI生成的活动</h2>
    
    <div class="split-view">
        <div class="ai-generated">
            <h3>AI生成内容</h3>
            <div id="ai-content">
                <!-- 显示AI生成的问题、选项 -->
            </div>
        </div>
        
        <div class="teacher-edit">
            <h3>编辑和优化</h3>
            <form id="review-form">
                <input type="text" name="title" placeholder="修改标题">
                <textarea name="question" placeholder="修改问题"></textarea>
                <!-- 可编辑的选项 -->
                
                <div class="actions">
                    <button type="button" class="btn-accept">✅ 接受</button>
                    <button type="button" class="btn-regenerate">🔄 重新生成</button>
                    <button type="submit" class="btn-save">💾 保存修改</button>
                </div>
            </form>
        </div>
    </div>
</div>
```

#### 1.2 更多AI功能

1. **智能评分** - AI辅助评判简答题
2. **学习路径推荐** - 基于学生表现推荐下一步学习内容
3. **自动摘要** - 自动生成活动结果摘要
4. **智能分组** - AI建议分组讨论成员

---

### 2. 通知系统

#### 2.1 实时通知

**新增文件**: `services/notification_service.py`

```python
class NotificationService:
    """通知服务"""
    
    COLLECTION_NAME = 'notifications'
    
    @staticmethod
    def send_notification(user_id, title, message, type='info'):
        """
        发送通知
        
        type: info, success, warning, error
        """
        pass
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        """获取用户通知"""
        pass
    
    @staticmethod
    def mark_as_read(notification_id):
        """标记为已读"""
        pass
```

#### 2.2 通知触发场景

- 📚 教师发布新活动 → 通知已注册学生
- ✅ 学生提交回答 → 通知教师
- 🏆 获得成就/徽章 → 通知学生
- 📊 报告生成完成 → 通知教师
- ⏰ 活动即将截止 → 提醒学生

---

### 3. 徽章和成就系统

**新增文件**: `models/achievement.py`

```python
class Achievement:
    """成就徽章系统"""
    
    ACHIEVEMENTS = {
        'first_activity': {
            'name': '初次尝试',
            'description': '完成第一个活动',
            'icon': '🎯'
        },
        'quiz_master': {
            'name': '测验大师',
            'description': '连续5次测验满分',
            'icon': '🏆'
        },
        'active_learner': {
            'name': '活跃学习者',
            'description': '连续7天参与活动',
            'icon': '🔥'
        },
        'top_performer': {
            'name': '顶尖表现',
            'description': '进入排行榜前3名',
            'icon': '⭐'
        }
    }
    
    @staticmethod
    def check_and_award(student_id):
        """检查并授予成就"""
        pass
```

---

## 📱 第四阶段：移动应用开发（优先级：🔵 低）

### PWA（渐进式Web应用）

将系统转换为PWA，支持：
- 📱 添加到主屏幕
- 🔄 离线访问
- 🔔 推送通知
- 📶 网络状态处理

**新增文件**: `static/manifest.json`

```json
{
  "name": "PolyU Learning Activity System",
  "short_name": "PolyU LAS",
  "description": "互动学习活动平台",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4CAF50",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

## 🚀 实施优先级和时间规划

### Phase 1（1-2周）- 核心功能补全
- [ ] Quiz小测验功能（5天）
- [ ] CSV批量导入学生（2天）
- [ ] 排行榜基础功能（3天）
- [ ] 响应式UI基础（3天）

### Phase 2（1周）- 小游戏和可视化
- [ ] 小游戏模块（4天）
- [ ] 数据可视化图表（3天）

### Phase 3（1周）- 用户体验
- [ ] AI审核界面（2天）
- [ ] 通知系统（2天）
- [ ] 成就徽章（2天）
- [ ] 移动端优化（1天）

### Phase 4（可选）- 高级功能
- [ ] 报告导出（2天）
- [ ] PWA支持（3天）
- [ ] 高级分析（3天）

---

## 📋 接下来的步骤

您希望我现在开始实施哪个功能模块？建议优先级：

1. **🔴 最优先**: Quiz小测验功能（学生和教师都急需）
2. **🔴 高优先**: CSV批量导入学生（教师管理需求）
3. **🔴 高优先**: 排行榜系统（提高学生参与度）
4. **🔴 高优先**: 响应式UI（移动设备支持）
5. **🟡 中优先**: 小游戏模块
6. **🟡 中优先**: 数据可视化增强

请告诉我您想先实现哪个功能，我将立即开始编码！ 🚀
