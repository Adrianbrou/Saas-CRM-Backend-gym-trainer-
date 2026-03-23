# Gym CRM — Task Tracker

## PHASE 1 — Database Layer ✅ COMPLETE

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
- [x] `models/__init__.py` — imports all models so Alembic can find them
- [x] Delete `models/trainer.py` (empty, replaced by Staff)
- [x] Delete `models/personal_training.py` (empty, wrong concept)

### Alembic Migrations

- [x] Initialize Alembic (`alembic init migrations`)
- [x] Configure `migrations/env.py` — sys.path fix, Base.metadata, DATABASE_URL from .env
- [x] Run first migration (`alembic revision --autogenerate -m "initial tables"`)
- [x] Apply migration (`alembic upgrade head`)
- [x] Verify all 9 tables exist in PostgreSQL

---

## PHASE 2 — Repository Layer ✅ COMPLETE

- [x] `repository/gym_repository.py` — create, get_by_id, get_all, update, delete
- [x] `repository/member_repository.py` — + get_by_email, get_all filters by gym_id
- [x] `repository/staff_repository.py` — + get_by_email, get_all filters by gym_id
- [x] `repository/workout_repository.py` — + get_by_body_part, no gym_id filter
- [x] `repository/workout_session_repository.py` — + get_by_trainer, filters by gym_id
- [x] `repository/progress_repository.py` — + get_by_member, get_by_workout, get_by_session_id

---

## PHASE 3 — Schemas (Pydantic) ✅ COMPLETE

- [x] `schemas/gym.py` — GymCreate, GymUpdate, GymResponse
- [x] `schemas/member.py` — MemberCreate, MemberUpdate, MemberResponse
- [x] `schemas/staff.py` — StaffCreate, StaffUpdate, StaffResponse + RoleEnum
- [x] `schemas/workout.py` — WorkoutCreate/Update/Response + BodyPartCreate/Update/Response
- [x] `schemas/workout_session.py` — WorkoutSessionCreate/Update/Response + Attendance + SessionWorkouts
- [x] `schemas/progress.py` — ProgressCreate, ProgressUpdate, ProgressResponse

---

## PHASE 4 — Service Layer ✅ COMPLETE

- [x] `services/gym_service.py` — register_gym, update_gym, get_gym, delete_gym
- [x] `services/member_service.py` — register_member, update_member, get_member, delete_member
- [x] `services/staff_service.py` — register_staff, update_staff, get_staff, delete_staff
- [x] `services/workout_service.py` — create_workout, get_workout, update_workout, delete_workout
- [x] `services/workout_session_service.py` — create_session, add_member_to_session, remove_member_from_session
- [x] `services/progress_service.py` — log_progress, get_progress, update_progress, delete_progress, get_by_member/workout/session

---

## PHASE 5 — API Layer ✅ COMPLETE

- [x] `database/session.py` — get_db dependency added (yield SessionLocal, finally close)
- [x] `api/gyms.py` — POST, GET all, GET by id, PATCH, DELETE — all complete and tested
- [x] `api/members.py` — CRUD endpoints + GET /members/gyms/{gym_id}
- [x] `api/staff.py` — CRUD endpoints + GET /staff/gym/{gym_id} (route conflict fix)
- [x] `api/workouts.py` — CRUD endpoints (global scope, not gym-scoped)
- [x] `api/workout_sessions.py` — create session, list by gym, add/remove member attendance
- [x] `api/progress.py` — log, get, update, delete + filter by member/workout/session
- [x] `main.py` — all 6 routers registered

---

## PHASE 6 — Authentication & Security

- [x] `core/security.py` — bcrypt password hashing + verify + JWT create/decode
- [x] `models/Staff.py` — hashed_password column added (nullable=True) + migration applied
- [x] `schemas/staff.py` — password field added to StaffCreate (not exposed in StaffResponse)
- [x] `services/staff_service.py` — hashes password before saving, pops plain password
- [x] `api/auth.py` — POST /auth/login → JWT token (email + gym_id + password)
- [x] `main.py` — auth_router registered
- [x] `core/dependency.py` — get_current_user dependency (decode JWT → return Staff)
- [x] Role-based access control (manager vs trainer permissions)
- [x] Protect routes with Depends(get_current_user)

---

## PHASE 7 — Background Tasks & Email

- [x] Welcome email on member registration (FastAPI BackgroundTasks)
- [x] Session notification dispatch
- [x] Structured logging setup

---

## PHASE 8 — Performance

- [ ] Redis caching for gym stats/dashboard (deferred to Phase 10 — will use Docker)
- [x] Pagination on all list endpoints
- [x] Remove `echo=True` from engine for production
- [x] Query optimization review

---

## PHASE 9 — Testing

- [x] Setup pytest + test database (SQLite in-memory via conftest.py)
- [x] Unit tests for each service (19 tests, all passing)
  - [x] test_gyms.py — happy path, duplicate, not found
  - [x] test_members.py — happy path, duplicate, not found
  - [x] test_staff.py — happy path, duplicate, not found (verify_password)
  - [x] test_workout.py — happy path, duplicate, not found (BodyPart seed)
  - [x] test_workout_session.py — happy path, trainer not found, member not found
  - [x] test_progress.py — happy path, not found, empty list, update not found
- [x] Alembic seed migration for BodyParts (9 body parts)
- [x] pytest.ini with pythonpath = .
- [x] Integration tests — COMPLETE (32 tests across all 6 API files)
  - [x] test_api_gyms.py — create, get, not found, duplicate, update, delete
  - [x] test_api_members.py — create, get, not found, duplicate, update, delete
  - [x] test_api_staff.py — create, get, not found, duplicate, update, delete
  - [x] test_api_workouts.py — create, get, not found, duplicate, update, delete
  - [x] test_api_workout_sessions.py — create, trainer not found, add/remove member
  - [x] test_api_progress.py — log, get, not found, update, delete
- [x] Fixed status codes — all GET/PATCH/DELETE not-found return 404 (was 400)
- [x] Email errors silenced in tests (try/except in core/email.py)
- [x] Health check endpoint (`/health`) — GET /health returns {"status": "ok"}, no auth

---

## PHASE 10 — Deployment

- [x] `Dockerfile`
- [x] `docker-compose.yml` (app + PostgreSQL)
- [x] Project restructure (source moved into app/ subfolder — PYTHONPATH fixed permanently)
  - [x] Deleted root-level __init__.py
  - [x] Updated load_dotenv paths in engine.py, email.py, security.py
  - [x] Updated Dockerfile CMD and removed ENV PYTHONPATH
  - [x] Updated CI — removed symlink step, fixed py_compile path
  - [x] Updated migrations/env.py sys.path (3 levels → 2 levels)
  - [x] 52/52 tests passing after restructure
- [ ] Redis caching (app + PostgreSQL + Redis in docker-compose)
- [ ] Full CI/CD pipeline (deploy on green)
- [ ] Deploy to cloud (AWS / GCP / Azure)
