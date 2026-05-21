# Habit Tracker API 🚀

Backend API for a fullstack Habit Tracker application built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **JWT Authentication**, and **Docker**.

This API handles user authentication, habit management, daily habit completions, streak calculation, and dashboard statistics.

---

## ✨ Features

- 🔐 JWT authentication
- 👤 User registration and login
- ✅ Habit CRUD
- 📅 Daily habit completion tracking
- 🔥 Streak calculation
- 📊 Habit statistics
- 🧩 User-based data isolation
- 🗄 PostgreSQL database
- 🔄 Alembic migrations
- 🐳 Dockerized development environment

---

## 🛠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Python-Jose
- Passlib + Bcrypt
- Docker
- Docker Compose

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/CarmenOrtiz12/habit-tracker.git
cd habit-tracker
```

### 2. Create `.env` file:

```env
DATABASE_URL=value
SECRET_KEY=value
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=value
```

### 3. Run backend with Docker:

```bash
docker compose up --build
```

Backend available at: http://localhost:8000

Swagger docs: http://localhost:8000/docs

---

## 🧬 Database migrations

Create migration:

```bash
docker compose exec api alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
docker compose exec api alembic upgrade head
```

---

## 🔑 Authentication

Login uses OAuth2 password flow: POST /login

Protected endpoints require: Authorization = Bearer <token>

## 👩‍💻 Author

Built by María Del Carmen Ortiz Garcia.