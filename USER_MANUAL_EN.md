# 📚 Learning Activity Management System - User Manual (EN)

## Table of Contents

1.  [System Overview](#1-system-overview)
2.  [System Architecture](#2-system-architecture)
3.  [Database Design](#3-database-design)
4.  [User Roles & Permissions](#4-user-roles--permissions)
5.  [Feature Walkthrough](#5-feature-walkthrough)
    -   [Administrator Features](#51-administrator-features)
    -   [Teacher Features](#52-teacher-features)
    -   [Student Features](#53-student-features)
6.  [Getting Started Guide](#6-getting-started-guide)
7.  [Frequently Asked Questions (FAQ)](#7-frequently-asked-questions-faq)

---

## 1. System Overview

### 1.1. Project Introduction

The Learning Activity Management System is a web-based educational platform designed to foster teacher-student interaction and provide intelligent management of learning activities. The system supports multiple activity types and integrates AI-powered features to streamline the educational process.

### 1.2. Core Features

-   ✅ **Multi-Role Support**: Dedicated interfaces and permissions for Administrators, Teachers, and Students.
-   🤖 **AI-Driven**: Powered by GPT-4o-mini for automatic activity generation and intelligent response evaluation.
-   📊 **Diverse Activity Types**: Supports Polls, Short Answer questions, and Word Clouds.
-   🎮 **Gamified Design**: Includes a points system, leaderboards, and achievement badges to boost engagement.
-   📱 **Responsive Interface**: Fully functional on both desktop and mobile devices.
-   🔐 **Secure & Reliable**: Features password encryption, session management, and robust permission controls.

### 1.3. Technology Stack

| Category      | Technology                               |
|---------------|------------------------------------------|
| **Backend**   | Python 3.13, Flask 3.0.0                 |
| **Frontend**  | HTML5, CSS3, JavaScript (ES6), Bootstrap |
| **Database**  | MongoDB (NoSQL)                          |
| **AI Service**| OpenAI GPT-4o-mini                       |
| **Deployment**| Vercel                                   |

---

## 2. System Architecture

### 2.1. Architectural Overview

The system follows a monolithic architecture with a Model-View-Controller (MVC) pattern, enhanced by a Service Layer for better separation of concerns.

```
+-----------------------------------------------------------------+
|                        User Interface (Client)                  |
+---------------------------------^-------------------------------+
                                  | (HTTP Requests)
+---------------------------------v-------------------------------+
|                     Web Server (Flask Application)              |
|                                                                 |
|    +-------------------------+    +-------------------------+   |
|    |     Routes (Controller) |    |   Templates (View)      |   |
|    +-------------------------+    +-------------------------+   |
|                 |                              ^                |
|                 v                              |                |
|    +-------------------------------------------------------+    |
|    |                  Service Layer                        |    |
|    +-------------------------------------------------------+    |
|                 |                              ^                |
|                 v                              |                |
|    +-------------------------------------------------------+    |
|    |                    Model Layer                        |    |
|    +-------------------------------------------------------+    |
|                                |                                |
+--------------------------------v--------------------------------+
                                 | (Database Queries)
+--------------------------------v--------------------------------+
|                     Database (MongoDB)                          |
+-----------------------------------------------------------------+
```

### 2.2. Directory Structure

```
groupproject-team_3/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration file
├── models/                     # Data models (User, Course, Activity)
├── routes/                     # Flask Blueprints (Controllers)
├── services/                   # Business logic layer
├── templates/                  # HTML templates (Views)
└── static/                     # Static assets (CSS, JS)
```

---

## 3. Database Design

The system uses MongoDB, a NoSQL database, for its flexible schema, which is ideal for handling diverse activity types.

### 3.1. Core Collections

1.  **Users**: Stores administrator and teacher accounts.
    -   Fields: `username`, `email`, `password_hash`, `role` (`admin`/`teacher`).
2.  **Courses**: Stores course information.
    -   Fields: `name`, `code` (unique), `description`, `teacher_id`.
3.  **Activities**: Stores details for all learning activities.
    -   Fields: `title`, `type`, `course_id`, `link`.
    -   `content`: A sub-document with a structure that varies by activity `type`.
    -   `responses`: An embedded array of student submissions, including the answer, points, and AI evaluation.
4.  **Students**: Stores student enrollment data.
    -   Fields: `student_id`, `name`, `email`, `course_id`, `points`, `badges`.

---

## 4. User Roles & Permissions

| Role          | Access Level | Primary Functions                                       |
|---------------|--------------|---------------------------------------------------------|
| 👑 **Admin**  | Highest      | System oversight, user management, data integrity.      |
| 👨‍🏫 **Teacher**| Medium       | Course creation, activity management, student grading.  |
| 👨‍🎓 **Student**| Basic        | Participating in activities, viewing scores and ranks.  |

### Permission Matrix

| Feature               | Admin | Teacher | Student |
|-----------------------|:-----:|:-------:|:-------:|
| Manage Users          |   ✅   |    ❌    |    ❌    |
| Manage All Courses    |   ✅   |    ❌    |    ❌    |
| Create/Manage Own Courses |   ✅   |    ✅    |    ❌    |
| Create Activities     |   ✅   |    ✅    |    ❌    |
| Participate in Activities |   ❌   |    ❌    |    ✅    |
| View All Results      |   ✅   |    ✅    |    ✅    |
| View Leaderboard      |   ❌   |    ✅    |    ✅    |

---

## 5. Feature Walkthrough

### 5.1. Administrator Features

#### Admin Dashboard (`/admin`)
-   **System Statistics**: View total counts of teachers, activities, and students.
-   **Quick Actions**: Navigate quickly to manage users, activities, or courses.

#### User Management (`/admin/users`)
-   **View & Search**: See a list of all users and search by username or email.
-   **Create Users**: Create new teacher or administrator accounts.
-   **Edit & Delete**: Modify user details or remove accounts from the system.

#### Course Management (`/admin/courses`)
-   **View All Courses**: Browse a comprehensive list of all courses across the system.
-   **Edit Courses**: Modify course details, such as name, description, or assigned teacher.
-   **Delete Courses**: Permanently remove a course and all its associated data (activities, enrollments). This action is irreversible and requires confirmation.

### 5.2. Teacher Features

#### Teacher Dashboard (`/dashboard`)
-   **Overview**: See a summary of your courses, total students, and activities.
-   **Course List**: Access each of your courses to view details or create new activities.

#### Course Creation (`/course/create`)
1.  Fill in the **Course Name**, a unique **Course Code**, and an optional **Description**.
2.  Click "Create Course". The system will generate the course and provide the code for students to register.

#### Importing Students
1.  From the course details page, click "Import Students".
2.  Prepare a CSV file with the columns: `student_id`, `name`, `email`.
3.  Upload the file to bulk-enroll students into your course.

#### Creating Activities (`/activity/create`)

**A. Manual Creation**
-   **Select Course & Type**: Choose the course and activity type (Poll, Short Answer, Word Cloud).
-   **Fill in Details**:
    -   **Poll**: Write a question and provide at least two options.
    -   **Short Answer**: Write a question and set an optional word limit.
    -   **Word Cloud**: Write a prompt for students to submit keywords.
-   **Create**: Click "Create Activity" to finalize.

**B. AI-Assisted Creation 🤖**
1.  **Select "AI-Assisted"**: Switch to the AI generation tab.
2.  **Provide Context**: Either paste text directly or upload a document (PDF, TXT).
3.  **Generate**: Click "Generate with AI". The system will send the context to GPT-4o-mini.
4.  **Preview & Create**: The AI will generate relevant questions and content based on your input. Review the generated activity and click "Create Activity".

#### Viewing Activity Results (`/activity/{id}`)
-   **Live Dashboard**: See student responses as they come in.
-   **Polls**: View a bar chart of the option distribution.
-   **Short Answers**: Read each student's answer and view the detailed **AI Evaluation**, which includes a score, qualitative feedback, strengths, and areas for improvement.
-   **Word Clouds**: See a visual representation of the most frequently submitted keywords.

### 5.3. Student Features

#### Student Dashboard (`/student/dashboard`)
-   **At a Glance**: View your total points, rank, and badges.
-   **Pending Activities**: See a list of activities you need to complete, along with their deadlines.
-   **Recent Submissions**: Review your most recent activity submissions and scores.

#### Enrolling in a Course
1.  Navigate to "Browse Courses".
2.  Enter the unique **Course Code** provided by your teacher.
3.  Click "Register" to join the course.

#### Participating in an Activity
-   Access activities via your dashboard or a direct link from your teacher.
-   **Polls**: Select your answer and submit. You'll see immediately if you were correct.
-   **Short Answers**: Type your response and submit. The AI will evaluate it instantly and provide detailed feedback and a score.
-   **Word Clouds**: Enter relevant keywords and submit.

#### Leaderboard & Profile
-   **Leaderboard**: See how you rank against your classmates in a course-specific leaderboard based on total points.
-   **Profile**: View your overall statistics, including all earned badges and your points history.

---

## 6. Getting Started Guide

### Quick Start for Teachers (5 Minutes)

1.  **Log In**: Use the credentials provided by your administrator.
2.  **Create a Course**: Go to your dashboard, click "New Course", and fill in the details. Note the **Course Code**.
3.  **Enroll Students**: Share the course code with your students or use the "Import Students" feature with a CSV file.
4.  **Create an Activity**:
    -   **Easy Mode (AI)**: Go to "Create Activity", select "AI-Assisted", paste your lesson material, and let the AI do the work.
    -   **Manual Mode**: Select "Manual Create", choose an activity type, and write your own questions.
5.  **Share & Monitor**: Copy the activity link and share it. Watch the results come in live from the activity details page.

### Quick Start for Students (3 Minutes)

1.  **Log In**: Use the credentials provided by your teacher.
2.  **Join a Course**: Go to "Browse Courses" and enter the **Course Code** from your teacher.
3.  **Do an Activity**: Go to your dashboard, find an activity, and click "Start".
4.  **Submit & Learn**: Answer the questions and click "Submit". For short answers, review the instant AI feedback to see how you did.
5.  **Check Your Rank**: Visit the "Leaderboard" to see your progress!

---

## 7. Frequently Asked Questions (FAQ)

**Q: How do I get an account?**
-   **A:** Teachers and administrators must be created by an existing administrator. Students are typically enrolled by their teacher via CSV import or can self-register for a course if they have the code.

**Q: I forgot my password. What should I do?**
-   **A:** Please contact your system administrator to have your password reset.

**Q: Is the AI evaluation accurate?**
-   **A:** The AI evaluation (powered by GPT-4o-mini) is highly accurate for its intended purpose of providing formative feedback. However, teachers always have the final say and can review the AI's assessment.

**Q: Can I edit an activity after creating it?**
-   **A:** To ensure data consistency, activities cannot be edited once they have responses. It is recommended to delete the activity and create a new one if significant changes are needed.

**Q: What browsers are supported?**
-   **A:** The system is compatible with all modern web browsers, including Chrome, Firefox, Safari, and Edge.

---
*This document is for educational and reference purposes. Last updated: November 13, 2025.*
