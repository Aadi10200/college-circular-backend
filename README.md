# College Circular Management System (Backend)

A production-ready backend system for managing college circulars with role-based authentication, approval workflows, targeted visibility, and attachment support. Built to demonstrate real-world backend engineering and system design.

---

## 🚀 Project Overview

The **College Circular Management System** is a backend-only application designed for colleges to publish and manage circulars efficiently while ensuring that students only see circulars relevant to them.

Instead of “sending” circulars, the system **stores circulars centrally** and allows students to **fetch applicable circulars dynamically** based on their branch, year, and section.

This project focuses on:

* Clean REST API design
* Proper database modeling
* Secure authentication & authorization
* Real-world approval flows
* Production deployment

---

## 🧠 Key Concepts Demonstrated

* RESTful API design with correct HTTP methods
* JWT-based authentication (stateless, expirable tokens)
* Role-based authorization (ADMIN / STUDENT)
* Approval-based access control
* Hierarchical data modeling
* Targeted data visibility (scope-based access)
* File upload handling (attachments)
* Production deployment on Render

---

## 🏗️ System Architecture

### Data Hierarchy

```
Branch → Year → Section → Student
```

* **Branch**: CSE, CSE AI-ML, Mechanical, etc.
* **Year**: 1–4 (scoped per branch)
* **Section**: A / B / C (scoped per year)
* **Student**: Belongs to exactly one section

Uniqueness is enforced **within parent scope**, not globally.

---

## 🗃️ Database Design

### Branch

* `branch_id` (PK)
* `branch_name` (unique)

### Year

* `year_id` (PK)
* `year_name`
* `branch_id` (FK)
* **Unique**: (`year_name`, `branch_id`)

### Section

* `section_id` (PK)
* `section_name`
* `year_id` (FK)
* **Unique**: (`section_name`, `year_id`)

### Student

* `student_id` (PK)
* `name`
* `roll_no`
* `section_id` (FK)
* **Unique**: (`roll_no`, `section_id`)

---

## 🔐 Authentication & Authorization

### User Roles

* **ADMIN** – manages branches, students, and circulars
* **STUDENT** – views and interacts with circulars

### Approval Flow

1. User signs up → status = `PENDING`
2. Admin approves and links `user_id` ↔ `student_id`
3. Status becomes `ACTIVE`
4. Student logs in again to receive updated JWT

### JWT Payload

* `user_id`
* `role`
* `status`

### Middleware

* `@jwt_required()` – authentication
* `@required_role("ADMIN")` – admin-only APIs
* `@require_active_students` – approved students only

---

## 📢 Circular System

### Core Insight

Circulars are **stored**, not pushed. Students **fetch** circulars applicable to them.

### Circular Targeting

Controlled via `CircularTarget` table:

| Scope   | branch_id | year_id | section_id |
| ------- | --------- | ------- | ---------- |
| Global  | NULL      | NULL    | NULL       |
| Branch  | ✔         | NULL    | NULL       |
| Year    | NULL      | ✔       | NULL       |
| Section | NULL      | NULL    | ✔          |

### Read / Unread Tracking

* Implemented using `StudentCircularStatus`
* Each student sees per-circular read state

### Attachments

* Multiple attachments per circular
* Stored on disk, not database
* Supported types: PDF, PNG, JPG, JPEG

---

## 🌐 REST API Endpoints (Highlights)

### Auth

* `POST /auth/signup`
* `POST /auth/login`

### Admin

* `POST /branches`
* `POST /years`
* `POST /sections`
* `POST /students`
* `POST /circular`
* `POST /circular/<id>/targets`
* `POST /circular/<id>/attachments`

### Student

* `GET /student/<id>/circulars`
* `POST /student/<id>/circular/<id>/read`

IDs are always discovered via GET APIs — never hardcoded.

---

## 🚀 Deployment

* Platform: **Render**
* Runtime: Python + Gunicorn
* CI/CD: Auto-deploy on GitHub push
* Environment variables used for secrets

Live URL:

```
https://college-circular-backend.onrender.com
```

---

## 🧪 Testing

* End-to-end testing via Postman
* Verified:

  * Role-based access control
  * Approval flow
  * Circular targeting
  * Read/unread status
  * Attachments handling

---

## 🧑‍💻 Tech Stack

* Python
* Flask
* Flask-JWT-Extended
* SQLAlchemy
* SQLite (dev & demo)
* Gunicorn
* Render

---

## 📌 Author

Built by **Aaditya Singh Thakur** as a first-year backend engineering project.
