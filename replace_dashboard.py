"""
Replace dashboard.html with new version
"""

new_content = """{% extends "base.html" %}

{% block title %}Student Dashboard{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/student.css') }}">
{% endblock %}

{% block content %}
<div class="container">
    <!-- Welcome Header -->
    <div class="page-header">
        <div>
            <h1>👋 Welcome Back, {{ user.username }}!</h1>
            <p class="text-muted">Student ID: {{ user.student_id }} | {{ user.email }}</p>
        </div>
        <div>
            <button onclick="window.location.href='{{ url_for(\\'student.browse_courses\\') }}'" class="btn btn-primary">
                🔍 Browse Courses
            </button>
        </div>
    </div>

    <!-- Learning Progress Overview -->
    <div class="dashboard-stats">
        <div class="stat-card card-purple">
            <div class="stat-icon">📚</div>
            <div class="stat-content">
                <h3>{{ enrolled_courses|length }}</h3>
                <p>Enrolled Courses</p>
            </div>
        </div>

        <div class="stat-card card-blue">
            <div class="stat-icon">📝</div>
            <div class="stat-content">
                <h3>{{ total_activities }}</h3>
                <p>Total Activities</p>
            </div>
        </div>

        <div class="stat-card card-green">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
                <h3>{{ completed_activities }}</h3>
                <p>Completed</p>
            </div>
        </div>

        <div class="stat-card card-orange">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
                <h3>{{ completion_rate }}%</h3>
                <p>Completion Rate</p>
            </div>
        </div>
    </div>

    <!-- Main Content Grid -->
    <div class="dashboard-grid">
        <!-- My Courses Section -->
        <div class="dashboard-section">
            <div class="section-header">
                <h2>📚 My Courses</h2>
                <a href="{{ url_for(\\'student.my_courses\\') }}" class="btn-link">View All →</a>
            </div>

            {% if enrolled_courses %}
                <div class="course-list">
                    {% for course in enrolled_courses[:3] %}
                    <div class="course-card">
                        <div class="course-header">
                            <div>
                                <h3>{{ course.code }}</h3>
                                <p class="course-name">{{ course.name }}</p>
                            </div>
                            <span class="badge badge-primary">{{ course.activity_count }} Activities</span>
                        </div>
                        <div class="course-progress">
                            {% set progress = (course.get(\\'completed_activities\\', 0) / course.activity_count * 100) if course.activity_count > 0 else 0 %}
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" style="width: {{ progress }}%"></div>
                            </div>
                            <span class="progress-text">{{ progress|round|int }}% Complete</span>
                        </div>
                        <a href="{{ url_for(\\'student.course_detail\\', course_id=course._id) }}" class="btn btn-sm btn-outline">
                            View Details →
                        </a>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty-state">
                    <p>📭 You haven\\'t enrolled in any courses yet.</p>
                    <a href="{{ url_for(\\'student.browse_courses\\') }}" class="btn btn-primary">Browse Available Courses</a>
                </div>
            {% endif %}
        </div>

        <!-- Recent Activities Section -->
        <div class="dashboard-section">
            <div class="section-header">
                <h2>📝 Recent Activities</h2>
                <a href="{{ url_for(\\'student.my_activities\\') }}" class="btn-link">View All →</a>
            </div>

            {% if recent_activities %}
                <div class="activity-list">
                    {% for activity in recent_activities %}
                    <div class="activity-item">
                        <div class="activity-icon">
                            {% if activity.type == \\'poll\\' %}🗳️
                            {% elif activity.type == \\'word_cloud\\' %}☁️
                            {% else %}✍️{% endif %}
                        </div>
                        <div class="activity-content">
                            <h4>{{ activity.title }}</h4>
                            <p class="activity-meta">
                                <span class="course-badge">{{ activity.course_code }}</span>
                                <span class="type-badge">{{ activity.type|replace(\\'_\\', \\' \\')|title }}</span>
                            </p>
                        </div>
                        <div class="activity-actions">
                            {% if activity.completed %}
                                <span class="status-badge status-completed">✓ Completed</span>
                            {% else %}
                                <span class="status-badge status-pending">⏳ Pending</span>
                                <a href="{{ url_for(\\'student.view_activity\\', activity_id=activity._id) }}" 
                                   class="btn btn-sm btn-primary">Participate</a>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty-state">
                    <p>📭 No activities available yet.</p>
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Learning Analytics Section -->
    <div class="dashboard-section">
        <div class="section-header">
            <h2>📈 My Learning Analytics</h2>
        </div>
        
        <div class="analytics-grid">
            <div class="analytics-card">
                <h3>Activity Participation</h3>
                <div class="activity-breakdown">
                    <div class="breakdown-item">
                        <span class="breakdown-label">🗳️ Polls</span>
                        <div class="breakdown-bar">
                            {% set poll_count = recent_activities|selectattr(\\'type\\', \\'equalto\\', \\'poll\\')|list|length %}
                            <div class="breakdown-fill" style="width: {{ (poll_count / recent_activities|length * 100) if recent_activities else 0 }}%; background: #8b5cf6;"></div>
                        </div>
                        <span class="breakdown-count">{{ poll_count }}</span>
                    </div>
                    <div class="breakdown-item">
                        <span class="breakdown-label">☁️ Word Clouds</span>
                        <div class="breakdown-bar">
                            {% set wc_count = recent_activities|selectattr(\\'type\\', \\'equalto\\', \\'word_cloud\\')|list|length %}
                            <div class="breakdown-fill" style="width: {{ (wc_count / recent_activities|length * 100) if recent_activities else 0 }}%; background: #ec4899;"></div>
                        </div>
                        <span class="breakdown-count">{{ wc_count }}</span>
                    </div>
                    <div class="breakdown-item">
                        <span class="breakdown-label">✍️ Short Answers</span>
                        <div class="breakdown-bar">
                            {% set sa_count = recent_activities|selectattr(\\'type\\', \\'equalto\\', \\'short_answer\\')|list|length %}
                            <div class="breakdown-fill" style="width: {{ (sa_count / recent_activities|length * 100) if recent_activities else 0 }}%; background: #3b82f6;"></div>
                        </div>
                        <span class="breakdown-count">{{ sa_count }}</span>
                    </div>
                </div>
            </div>

            <div class="analytics-card">
                <h3>Quick Actions</h3>
                <div class="quick-actions">
                    <a href="{{ url_for(\\'student.browse_courses\\') }}" class="quick-action-btn">
                        <span class="action-icon">🔍</span>
                        <span>Browse Courses</span>
                    </a>
                    <a href="{{ url_for(\\'student.my_activities\\') }}" class="quick-action-btn">
                        <span class="action-icon">📝</span>
                        <span>My Activities</span>
                    </a>
                    <a href="{{ url_for(\\'student.leaderboard\\') }}" class="quick-action-btn">
                        <span class="action-icon">🏆</span>
                        <span>Leaderboard</span>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
/* Dashboard Layout */
.dashboard-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.card-purple { border-left: 4px solid #8b5cf6; }
.card-blue { border-left: 4px solid #3b82f6; }
.card-green { border-left: 4px solid #10b981; }
.card-orange { border-left: 4px solid #f59e0b; }

.stat-icon {
    font-size: 2.5rem;
}

.stat-content h3 {
    font-size: 2rem;
    font-weight: bold;
    color: #1f2937;
    margin: 0;
}

.stat-content p {
    color: #6b7280;
    margin: 0;
    font-size: 0.875rem;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
}

.dashboard-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.section-header h2 {
    font-size: 1.5rem;
    color: #1f2937;
    margin: 0;
}

.btn-link {
    color: #3b82f6;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.btn-link:hover {
    color: #2563eb;
}

/* Course Cards */
.course-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.course-card {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1rem;
    transition: border-color 0.2s;
}

.course-card:hover {
    border-color: #3b82f6;
}

.course-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.course-header h3 {
    font-size: 1rem;
    color: #3b82f6;
    margin: 0;
    font-weight: 600;
}

.course-name {
    color: #4b5563;
    margin: 0.25rem 0 0 0;
    font-size: 0.875rem;
}

.course-progress {
    margin-bottom: 1rem;
}

.progress-bar-container {
    width: 100%;
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    transition: width 0.3s;
}

.progress-text {
    font-size: 0.75rem;
    color: #6b7280;
}

/* Activity List */
.activity-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.activity-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    transition: background 0.2s;
}

.activity-item:hover {
    background: #f9fafb;
}

.activity-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.activity-content {
    flex: 1;
    min-width: 0;
}

.activity-content h4 {
    font-size: 0.938rem;
    color: #1f2937;
    margin: 0 0 0.25rem 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.activity-meta {
    display: flex;
    gap: 0.5rem;
    margin: 0;
}

.course-badge, .type-badge {
    font-size: 0.75rem;
    padding: 0.125rem 0.5rem;
    border-radius: 9999px;
    font-weight: 500;
}

.course-badge {
    background: #dbeafe;
    color: #1e40af;
}

.type-badge {
    background: #f3f4f6;
    color: #4b5563;
}

.activity-actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.status-badge {
    font-size: 0.75rem;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-weight: 500;
}

.status-completed {
    background: #d1fae5;
    color: #065f46;
}

.status-pending {
    background: #fef3c7;
    color: #92400e;
}

/* Analytics Section */
.analytics-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
}

.analytics-card {
    background: #f9fafb;
    border-radius: 8px;
    padding: 1.5rem;
}

.analytics-card h3 {
    font-size: 1.125rem;
    color: #1f2937;
    margin: 0 0 1rem 0;
}

.activity-breakdown {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.breakdown-item {
    display: grid;
    grid-template-columns: 120px 1fr 40px;
    align-items: center;
    gap: 1rem;
}

.breakdown-label {
    font-size: 0.875rem;
    color: #4b5563;
}

.breakdown-bar {
    height: 24px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
}

.breakdown-fill {
    height: 100%;
    transition: width 0.3s;
}

.breakdown-count {
    font-weight: 600;
    color: #1f2937;
    text-align: center;
}

.quick-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.quick-action-btn {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    text-decoration: none;
    color: #1f2937;
    font-weight: 500;
    transition: all 0.2s;
}

.quick-action-btn:hover {
    background: #f3f4f6;
    border-color: #3b82f6;
    color: #3b82f6;
}

.action-icon {
    font-size: 1.5rem;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 2rem;
    color: #6b7280;
}

.empty-state p {
    margin-bottom: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .dashboard-stats {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .analytics-grid {
        grid-template-columns: 1fr;
    }
    
    .page-header {
        flex-direction: column;
        gap: 1rem;
    }
}

@media (max-width: 480px) {
    .dashboard-stats {
        grid-template-columns: 1fr;
    }
    
    .breakdown-item {
        grid-template-columns: 80px 1fr 30px;
        gap: 0.5rem;
    }
}
</style>
{% endblock %}
"""

# Write to file
with open('templates/student/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Dashboard template replaced successfully!")
