# 🚀 DevFlow AI Backend

A scalable project management backend built with **Django REST Framework** that enables organizations to manage projects, tasks, team members, notifications, and activity tracking.

The application follows a **service-layer architecture**, implements **JWT authentication**, **role-based access control (RBAC)**, and includes **automated tests** to ensure reliability and maintainability.

---

# ✨ Features

## Authentication

- User Registration
- JWT Authentication
- User Profile
- Password Validation

## Organization Management

- Create organizations
- Invite members
- Update member roles
- Remove members
- Role-based permissions

## Project Management

- Create projects
- Update projects
- Delete projects
- Search projects
- Filter projects
- Ordering
- Pagination

## Task Management

- Create tasks
- Update tasks
- Delete tasks
- Assign team members
- Task priorities
- Task statuses
- Search tasks
- Filter tasks
- Ordering
- Pagination

## Task Comments

- Add comments
- Update comments
- Delete comments

## Task Attachments

- Upload attachments
- Delete attachments

## Activity Timeline

- Automatic activity logging
- Task history
- Project history

## Notifications

- Task assignment notifications
- Comment notifications
- Mark notification as read
- Mark all notifications as read

## Dashboard

Dashboard statistics including:

- Organizations
- Projects
- Tasks
- To Do Tasks
- In Progress Tasks
- Completed Tasks
- Unread Notifications

---

# 🛠 Tech Stack

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- drf-spectacular
- django-filter
- Factory Boy
- SQLite (Testing)
- Black
- isort
- Ruff

---

# 🏗 Architecture

The project follows a layered architecture.

```
View
│
├── Serializer
│
├── Service Layer
│
├── Models
│
└── Database
```

Business logic is separated from API views to improve maintainability and testability.

---

# 📁 Project Structure

```
devflow-ai/

apps/
│
├── accounts/
├── organizations/
├── projects/
├── tasks/
├── activities/
├── notifications/
├── dashboard/
├── common/
│
config/
│
manage.py
requirements.txt
README.md
```

---

# 🔐 Authentication

The API uses **JWT Authentication**.

After login you'll receive:

- Access Token
- Refresh Token

Include the access token in every request.

```
Authorization: Bearer <access_token>
```

---

## 📖 API Documentation

### Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

### ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

### OpenAPI Schema

```text
http://127.0.0.1:8000/api/schema/
```

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/Gayathrisanthosh978/devflow-ai.git

cd devflow-ai
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔧 Environment Variables

Create a `.env` file.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DATABASE_NAME=devflow

DATABASE_USER=postgres

DATABASE_PASSWORD=password

DATABASE_HOST=localhost

DATABASE_PORT=5432
```

---

# 🗄 Database

Run migrations

```bash
python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

---

# 🧪 Running Tests

Run all tests

```bash
python manage.py test
```

Current test status

```
69 Tests Passing
```

---

# 📦 Code Quality

Formatting

```bash
black .
```

Sort imports

```bash
isort .
```

Lint

```bash
ruff check .
```

---

# 🔒 Role-Based Access Control

Supported roles

- Owner
- Admin
- Project Manager
- Team Lead
- Developer
- QA
- Client

Permissions are enforced throughout the API.

---

# 🚀 Future Improvements

- Email invitations
- Real-time notifications using WebSockets
- Celery background jobs
- Redis caching
- Docker deployment
- CI/CD pipeline
- Kubernetes deployment
- Frontend application
- Analytics dashboard
- Time tracking
- Sprint management

---

# 📊 Project Highlights

- Clean Service Layer Architecture
- RESTful API Design
- JWT Authentication
- Role-Based Access Control
- Activity Logging
- Notification System
- Filtering
- Ordering
- Pagination
- OpenAPI Documentation
- Automated Testing
- Production-ready Code Style

---

# 👨‍💻 Author

**Gayathri Santhosh**

GitHub:
https://github.com/Gayathrisanthosh978

LinkedIn:
https://www.linkedin.com/in/gayathri-santhosh-020986191/