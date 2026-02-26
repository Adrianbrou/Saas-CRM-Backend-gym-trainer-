# Gym CRM — SaaS Backend API

A production-grade multi-tenant SaaS CRM backend built with **FastAPI** and **PostgreSQL**, designed for gym management. Each gym operates as an isolated tenant with its own staff, members, workout sessions, and progress tracking.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic |
| Auth | JWT + bcrypt |
| Cache | Redis |
| Containerization | Docker |
| Testing | Pytest |

---

## Architecture

```
Client → API → Service → Repository → Database
```

- **API layer** — thin, handles HTTP only
- **Service layer** — all business logic lives here
- **Repository layer** — all database queries isolated here
- **Models** — SQLAlchemy ORM mapped to PostgreSQL tables

---

## Domain Model

```
Gym (tenant)
├── Staff (role: manager | trainer)
└── Member
    └── Progress (weight, sets, reps per workout)

WorkoutSession
├── Staff (trainer running the session)
├── Members → via Attendance (link table)
└── Workouts → via SessionWorkouts (link table)

Workout
└── BodyPart (e.g. Chest, Legs, Back)
```

---

## Project Structure

```
app/
├── main.py
├── api/              # FastAPI routers (endpoints)
├── services/         # Business logic
├── repository/       # Database queries
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic input/output schemas
├── database/         # Engine, session, base
├── core/             # Security, JWT, hashing
├── middleware/        # Auth, logging, rate limiting
├── migrations/       # Alembic migration files
└── test/             # Pytest test suite
```

---

## Setup & Run

### 1. Clone and create virtual environment
```bash
git clone <repo-url>
cd app
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
Create a `.env` file in the `app/` folder:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/crm_db
```

### 4. Run database migrations
```bash
alembic upgrade head
```

### 5. Start the server
```bash
uvicorn main:app --reload
```

API available at: `http://localhost:8000`
Interactive docs at: `http://localhost:8000/docs`

---

## API Endpoints (planned)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/gyms` | Register a new gym |
| POST | `/members` | Register a member |
| POST | `/staff` | Add staff member |
| GET | `/members/{gym_id}` | List gym members |
| POST | `/sessions` | Create workout session |
| POST | `/sessions/{id}/attend` | Log member attendance |
| POST | `/progress` | Log workout progress |
| GET | `/progress/{member_id}` | Get member progress |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/health` | Health check |

---

## Roadmap

- [x] Phase 1 — Database layer (models, engine, migrations)
- [ ] Phase 2 — Repository layer
- [ ] Phase 3 — Pydantic schemas
- [ ] Phase 4 — Service layer
- [ ] Phase 5 — API endpoints
- [ ] Phase 6 — Authentication & JWT & RBAC
- [ ] Phase 7 — Background tasks & email
- [ ] Phase 8 — Redis caching & performance
- [ ] Phase 9 — Testing
- [ ] Phase 10 — Docker & deployment

---

## Key Features (planned)

- Multi-tenant isolation — each gym is fully isolated
- Role-based access control — manager vs trainer permissions
- JWT authentication
- Background email notifications
- Redis caching for dashboard metrics
- Paginated list endpoints
- Full test coverage
- Dockerized deployment

---

## Author

Built as a learning project following clean architecture principles used in production SaaS systems.
