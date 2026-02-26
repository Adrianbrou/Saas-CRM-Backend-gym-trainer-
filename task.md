# Gym CRM — Task Tracker

## PHASE 1 — Database Layer

### Setup
- [x] Fix engine.py — remove SQLite-only `check_same_thread`
- [x] Add RuntimeError guard for missing DATABASE_URL
- [x] Create `.env` with PostgreSQL connection string
- [x] Create `.gitignore`
- [x] Fix `database/base.py` typo (sqlachemy → sqlalchemy)

### Models
- [x] `models/gym.py` — Gym model with timestamps + relationships
- [x] `models/member.py` — Member model with FK, timestamps, relationship
- [x] `models/Staff.py` — Staff model with RoleEnum (manager/trainer)
- [x] `models/workout.py` — BodyPart + Workout (one-to-many)
- [x] `models/workout_session.py` — WorkoutSession + Attendance + SessionWorkouts
- [x] `models/progress.py` — Progress (weight/sets/reps per member per workout)
- [x] Delete `models/trainer.py` (empty, replaced by Staff)
- [x] Delete `models/personal_training.py` (empty, wrong concept)

### Migrations
- [x] Create `models/__init__.py` — import all models so Alembic can find them
- [ ] Initialize Alembic (`alembic init migrations`)
- [ ] Configure `migrations/env.py` — point to Base and DATABASE_URL
- [ ] Run first migration (`alembic revision --autogenerate -m "initial tables"`)
- [ ] Apply migration (`alembic upgrade head`)
- [ ] Verify all tables exist in PostgreSQL

---

## PHASE 2 — Repository Layer

- [ ] `repository/gym_repository.py` — create, get_by_id, get_all, update, delete
- [ ] `repository/member_repository.py`
- [ ] `repository/staff_repository.py`
- [ ] `repository/workout_repository.py`
- [ ] `repository/session_repository.py`
- [ ] `repository/progress_repository.py`

---

## PHASE 3 — Schemas (Pydantic)

- [ ] `schemas/gym.py` — GymCreate, GymUpdate, GymResponse
- [ ] `schemas/member.py` — MemberCreate, MemberUpdate, MemberResponse
- [ ] `schemas/staff.py` — StaffCreate, StaffUpdate, StaffResponse
- [ ] `schemas/workout.py`
- [ ] `schemas/session.py`
- [ ] `schemas/progress.py`

---

## PHASE 4 — Service Layer

- [ ] `services/gym_service.py` — register_gym
- [ ] `services/member_service.py` — register_member (check unique email per gym)
- [ ] `services/staff_service.py` — register_staff
- [ ] `services/session_service.py` — create_session, add_member, log_workout
- [ ] `services/progress_service.py` — log_progress

---

## PHASE 5 — API Layer

- [ ] `api/gyms.py` — CRUD endpoints
- [ ] `api/members.py` — CRUD endpoints
- [ ] `api/staff.py` — CRUD endpoints
- [ ] `api/workouts.py` — CRUD endpoints
- [ ] `api/sessions.py` — session management endpoints
- [ ] `api/progress.py` — progress logging endpoints
- [ ] Register all routers in `main.py`

---

## PHASE 6 — Authentication & Security

- [ ] `core/security.py` — bcrypt password hashing + verify
- [ ] JWT access token generation + validation
- [ ] `get_current_user` dependency
- [ ] Role-based access control (manager vs trainer permissions)
- [ ] Auth middleware

---

## PHASE 7 — Background Tasks & Email

- [ ] Welcome email on member registration (FastAPI BackgroundTasks)
- [ ] Session notification dispatch
- [ ] Structured logging setup

---

## PHASE 8 — Performance

- [ ] Redis caching for gym stats/dashboard
- [ ] Pagination on all list endpoints
- [ ] Remove `echo=True` from engine for production
- [ ] Query optimization review

---

## PHASE 9 — Testing

- [ ] Setup pytest + test database
- [ ] Unit tests for each service
- [ ] Integration tests for each API endpoint
- [ ] Health check endpoint (`/health`)

---

## PHASE 10 — Deployment

- [ ] `Dockerfile`
- [ ] `docker-compose.yml` (app + PostgreSQL + Redis)
- [ ] Environment config for production
- [ ] GitHub Actions CI/CD pipeline
- [ ] Deploy to cloud (AWS / GCP / Azure)
