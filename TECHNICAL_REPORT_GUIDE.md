# Technical Documentation for Learning Activity Management System

**Version**: 1.0.0  
**Last Updated**: November 13, 2025  
**Author**: GitHub Copilot

## Table of Contents
1. [Introduction](#1-introduction)
    - 1.1. Project Overview
    - 1.2. System Goals and Objectives
2. [System Architecture](#2-system-architecture)
    - 2.1. Architectural Style
    - 2.2. Component Breakdown
    - 2.3. Technology Stack
3. [Database Design and Schema](#3-database-design-and-schema)
    - 3.1. Database Choice: MongoDB
    - 3.2. Core Data Models
    - 3.3. ER Diagram
4. [Core Features and Functionality](#4-core-features-and-functionality)
    - 4.1. Role-Based Access Control (RBAC)
    - 4.2. Administrator Module
    - 4.3. Teacher Module
    - 4.4. Student Module
5. [User Interface (UI) and User Experience (UX)](#5-user-interface-ui-and-user-experience-ux)
    - 5.1. Design Philosophy
    - 5.2. Key UI Components
    - 5.3. User Flow Examples
6. [Technical Implementation Details](#6-technical-implementation-details)
    - 6.1. Backend Implementation
    - 6.2. Frontend Implementation
    - 6.3. AI Integration
    - 6.4. Deployment
7. [Key Design Decisions and Rationale](#7-key-design-decisions-and-rationale)
    - 7.1. Framework: Flask vs. Django
    - 7.2. Database: NoSQL (MongoDB) vs. SQL
    - 7.3. Data Structure: Embedded vs. Referenced Documents
    - 7.4. Rendering: Server-Side (Jinja2) vs. Client-Side (SPA)
8. [Conclusion and Future Work](#8-conclusion-and-future-work)

---

## 1. Introduction

### 1.1. Project Overview

The Learning Activity Management System is a web-based platform designed to enhance the educational experience by facilitating dynamic and interactive learning activities. It serves three primary user roles: Administrators, Teachers, and Students. The system leverages Artificial Intelligence to automate content creation and provide instant feedback, while incorporating gamification elements to boost student engagement.

### 1.2. System Goals and Objectives

- **To streamline activity management**: Provide teachers with tools to easily create, distribute, and manage learning activities.
- **To enhance student engagement**: Utilize gamification (points, leaderboards) and interactive activity types to motivate students.
- **To leverage AI for educational efficiency**: Integrate a Large Language Model (LLM) to assist in generating educational content and evaluating student responses.
- **To provide a scalable and maintainable platform**: Build a robust architecture that is easy to manage, extend, and deploy.

---

## 2. System Architecture

### 2.1. Architectural Style

The system is built upon a **Monolithic Architecture** using a modified **Model-View-Controller (MVC)** pattern. This choice provides simplicity in development and deployment, which is well-suited for the project's scope.

- **Model**: Represents the data structure. Located in the `models/` directory, these Python classes interface with the MongoDB database.
- **View**: The presentation layer, rendered as HTML. Located in the `templates/` directory, these files use the Jinja2 templating engine.
- **Controller**: Handles user input and business logic. Implemented as Flask Blueprints in the `routes/` directory, they process incoming requests and orchestrate responses.

A **Service Layer** (`services/`) is introduced to decouple business logic from the controllers, promoting code reusability and separation of concerns.

### 2.2. Component Breakdown

```
+-----------------------------------------------------------------+
|                        User Interface (Client)                  |
|              (HTML, CSS, JavaScript, Bootstrap)                 |
+---------------------------------^-------------------------------+
                                  | (HTTP Requests)
+---------------------------------v-------------------------------+
|                     Web Server (Flask Application)              |
|                                                                 |
|    +-------------------------+    +-------------------------+   |
|    |     Routes (Controller) |    |   Templates (View)      |   |
|    | (admin, auth, course,   |    | (Jinja2 HTML files)     |   |
|    |  activity, student)     |    |                         |   |
|    +-------------------------+    +-------------------------+   |
|                 |                              ^                |
|                 v                              |                |
|    +-------------------------------------------------------+    |
|    |                  Service Layer                        |    |
|    | (auth_service, db_service, genai_service, etc.)       |    |
|    +-------------------------------------------------------+    |
|                 |                              ^                |
|                 v                              |                |
|    +-------------------------------------------------------+    |
|    |                    Model Layer                        |    |
|    | (user.py, course.py, activity.py, student.py)         |    |
|    +-------------------------------------------------------+    |
|                                |                                |
+--------------------------------v--------------------------------+
                                 | (Database Queries)
+--------------------------------v--------------------------------+
|                     Database (MongoDB)                          |
+-----------------------------------------------------------------+
|                     External Service (OpenAI API)               |
+-----------------------------------------------------------------+
```

### 2.3. Technology Stack

| Category      | Technology                               | Rationale                                       |
|---------------|------------------------------------------|-------------------------------------------------|
| **Backend**   | Python 3.13, Flask 3.0.0                 | Rapid development, extensive libraries, simplicity. |
| **Frontend**  | HTML5, CSS3, JavaScript (ES6)            | Universal standards for web development.        |
| **Database**  | MongoDB                                  | Flexible schema for diverse activity types.     |
| **AI**        | OpenAI GPT-4o-mini                       | Strong balance of cost, speed, and capability.  |
| **Styling**   | Bootstrap                                | Responsive design and pre-built components.     |
| **Deployment**| Vercel                                   | Seamless Git integration, serverless functions. |

---

## 3. Database Design and Schema

### 3.1. Database Choice: MongoDB

MongoDB, a NoSQL database, was chosen for its schema flexibility. This is critical for the `activities` collection, where different activity types (`poll`, `short_answer`, `word_cloud`) require different data structures within the same collection. It also scales horizontally, which is beneficial for future growth.

### 3.2. Core Data Models

#### `users`
Stores administrator and teacher accounts.
- `username`, `email`, `password_hash`, `role` (`admin`/`teacher`), `active`

#### `courses`
Stores course information created by teachers.
- `name`, `code` (unique), `description`, `teacher_id` (references `users`), `active`

#### `students`
Stores student enrollment information for each course.
- `student_id`, `name`, `email`, `course_id` (references `courses`), `points`, `badges`

#### `activities`
The most complex collection, storing all activity details.
- `title`, `type`, `course_id`, `teacher_id`, `link` (unique access code)
- `content`: A sub-document whose structure varies by `type`.
- `responses`: An **embedded array** of student submissions. Each response includes `student_id`, `answer`, `submitted_at`, `points_earned`, and an optional `ai_evaluation` sub-document.

### 3.3. ER Diagram (Conceptual)

```
+----------+ 1      M +----------+
|  Users   |----------| Courses  |
| (Teacher)| teaches  |          |
+----------+          +----┬-----+
                           | 1
                           |
                           | M
                      +----▼-----+
                      |Activities|
                      +----┬-----+
                           |
                           | M (enrolls)
                           |
                      +----▼-----+
                      | Students |
                      +----------+
```
*Note: `Students` are scoped to a `Course`. `Activities` are also scoped to a `Course`.*

---

## 4. Core Features and Functionality

### 4.1. Role-Based Access Control (RBAC)

The system is built around three distinct roles, with functionality tailored to each. Authorization is managed via session cookies and decorator functions in Flask that check the user's role before granting access to a route.

### 4.2. Administrator Module

- **System Oversight**: A central dashboard provides at-a-glance statistics (user counts, activity distribution).
- **User Management**: Full CRUD (Create, Read, Update, Delete) capabilities for all user accounts, including the ability to create other administrators.
- **Course & Activity Management**: Admins can view and delete any course or activity in the system, ensuring data integrity and providing support for teachers. The course deletion cascades, removing associated activities and student enrollments.

### 4.3. Teacher Module

- **Dashboard**: A personalized dashboard showing the teacher's courses, student counts, and quick actions.
- **Course Management**: Teachers can create courses, which generates a unique course code for student registration.
- **Student Enrollment**: A streamlined process for bulk-adding students by uploading a CSV file.
- **Activity Creation**:
    - **Manual Mode**: Teachers have fine-grained control to define questions and options.
    - **AI-Assisted Mode**: Teachers can input raw text or upload a document (PDF, TXT). The system's `genai_service` communicates with the OpenAI API to automatically generate relevant questions, options, and key points based on the provided context.
- **Results Analysis**: A detailed view for each activity shows all student responses, scores, and AI-generated feedback.

### 4.4. Student Module

- **Dashboard**: A personalized view of pending activities, recent submissions, total points, and leaderboard rank.
- **Course Enrollment**: Students can browse and join courses using the unique code provided by their teacher.
- **Interactive Participation**:
    - **Polls**: Submit answers and receive immediate correctness feedback.
    - **Short Answer / Word Cloud**: Submit responses and receive instant, detailed AI-powered evaluation, including a score, qualitative feedback, strengths, and areas for improvement.
- **Gamification**:
    - **Points System**: Earn points for participation and correctness.
    - **Leaderboard**: A course-specific leaderboard fosters friendly competition.
    - **Badges**: Unlock achievements for milestones (e.g., "First Response," "Perfect Score").

---

## 5. User Interface (UI) and User Experience (UX)

### 5.1. Design Philosophy

The UI/UX design is guided by three principles:
1.  **Clarity**: Ensure that information is presented logically and actions are intuitive.
2.  **Efficiency**: Minimize the number of clicks required to complete common tasks.
3.  **Responsiveness**: Provide a seamless experience across devices (desktop, tablet, mobile) using a mobile-first approach.

### 5.2. Key UI Components

- **Dashboards**: Role-specific dashboards serve as the main entry point, providing relevant statistics and quick links.
- **Modals**: Used extensively for editing (users, courses) to avoid page reloads and keep the user in context.
- **Dynamic Forms**: The "Create Activity" form dynamically shows/hides fields based on the selected activity type, reducing clutter. HTML5 `required` attributes are managed via JavaScript to ensure correct validation.
- **Real-time Feedback Panels**: After a student submits a short answer, a dedicated panel appears with the AI's evaluation, using color-coding (green for high scores) and icons to improve readability.

### 5.3. User Flow Examples

#### A. Teacher Creates an AI-Assisted Activity

`Login` → `Dashboard` → `Select Course` → `Create Activity` → `Select "AI-Assisted"` → `Choose Activity Type (e.g., Poll)` → `Upload Document` → `Click "Generate with AI"` → `Preview & Confirm` → `Activity Created`

#### B. Student Participates in a Short Answer Activity

`Login` → `Dashboard` → `Select Pending Activity` → `Read Question` → `Type Answer in Textbox` → `Click "Submit"` → `View AI Feedback Panel` → `View Points Earned`

---

## 6. Technical Implementation Details

### 6.1. Backend Implementation

- **Flask Blueprints**: The application is modularized using Blueprints (`routes/`), with each file corresponding to a major feature area (e.g., `admin_routes.py`, `activity_routes.py`).
- **Database Abstraction**: The `services/db_service.py` acts as a lightweight Object-Document Mapper (ODM), providing a centralized interface for all database operations (e.g., `find_one`, `insert_one`). This isolates the application from the raw PyMongo driver.
- **Error Handling**: Custom error pages and JSON responses for API errors are configured to provide a consistent user experience.

### 6.2. Frontend Implementation

- **Jinja2 Templating**: All HTML is rendered server-side using Jinja2, which allows for template inheritance (`base.html`) and embedding Python logic directly into the markup.
- **AJAX with Fetch API**: Asynchronous actions, such as submitting activities or deleting items from a list, are handled using the browser's `fetch` API. This prevents full-page reloads and provides a smoother UX. For example, the manual activity creation form is submitted via `fetch`, with JavaScript constructing the `FormData` object.
- **DOM Manipulation**: Vanilla JavaScript is used to dynamically update the UI in response to user actions (e.g., adding more poll options, displaying loading spinners, showing alert messages).

### 6.3. AI Integration

- **`genai_service.py`**: This service acts as a facade for the OpenAI API. It contains methods like `generate_activity_from_text` and `evaluate_student_answer`.
- **Prompt Engineering**: The service uses carefully crafted system prompts to guide the LLM's output.
    - For **generation**, the prompt instructs the model to create questions based on the provided text and return the output in a specific JSON format.
    - For **evaluation**, the prompt instructs the model to act as a helpful teaching assistant, assess the student's answer against the question and key points, and provide a score and structured feedback (strengths, improvements).

### 6.4. Deployment

- **Vercel**: The project is configured for deployment on Vercel.
- **`vercel.json`**: This configuration file rewrites all incoming requests to the main Flask application (`app.py`), effectively turning the Flask app into a serverless function. It also defines the Python runtime version.
- **Environment Variables**: Sensitive information like the `MONGODB_URI` and `GITHUB_TOKEN` are managed as environment variables in the Vercel project settings.

---

## 7. Key Design Decisions and Rationale

### 7.1. Framework: Flask vs. Django

- **Decision**: Chose **Flask**.
- **Rationale**: Flask is a micro-framework, offering flexibility and simplicity. It does not impose a rigid project structure, which was ideal for this project's iterative development. Its lightweight nature results in a smaller footprint, which is advantageous for serverless deployments. Django, while powerful, would have introduced unnecessary complexity with its built-in ORM and admin panel.

### 7.2. Database: NoSQL (MongoDB) vs. SQL

- **Decision**: Chose **MongoDB (NoSQL)**.
- **Rationale**: The primary driver was the need for a flexible schema. The `activities` collection must store different data structures for polls, short answers, and word clouds. A relational (SQL) database would require complex table joins or JSON columns, whereas MongoDB handles this natively with its document-based model.

### 7.3. Data Structure: Embedded vs. Referenced Documents

- **Decision**: **Embed** student `responses` within the `activities` document.
- **Rationale**: This design choice optimizes for the most common read pattern: fetching an activity and all its responses at once. It avoids the need for an additional database query (a `$lookup` or application-level join), improving performance for the activity results page. The trade-off is a larger document size, but this is acceptable as the number of responses per activity is unlikely to exceed MongoDB's 16MB document limit.

### 7.4. Rendering: Server-Side (Jinja2) vs. Client-Side (SPA)

- **Decision**: Chose **Server-Side Rendering (SSR) with Jinja2**.
- **Rationale**: SSR simplifies the architecture by keeping the rendering logic on the backend. It was sufficient for the project's requirements, as the need for complex, real-time UI updates was limited. Building a Single-Page Application (SPA) with a framework like React or Vue would have required a separate frontend build process and a more complex API, increasing development overhead without a proportional gain in functionality for this specific use case.

---

## 8. Conclusion and Future Work

The Learning Activity Management System successfully meets its objectives by providing a feature-rich, AI-enhanced platform for educators and students. The chosen architecture and technologies provide a solid foundation that is both functional and maintainable.

### Potential Future Work

- **Real-time Collaboration**: Integrate WebSockets to enable real-time features, such as live leaderboards and teachers seeing responses as they are submitted.
- **Advanced Analytics**: Develop a more sophisticated analytics dashboard for teachers to track student performance trends over time.
- **Expanded Activity Types**: Add support for more complex activities, such as matching, sequencing, or code-based questions.
- **Decoupled Frontend**: Migrate the frontend to a modern JavaScript framework (e.g., React, Vue) to create a more interactive and scalable user experience as the application grows.
