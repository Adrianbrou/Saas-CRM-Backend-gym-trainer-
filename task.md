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
