from fastapi import FastAPI
from app.api.gyms import router as gym_router
from app.api.staff import router as staff_router
from app.api.members import router as member_router
from app.api.progress import router as progress_router
from app.api.workout_sessions import router as workout_sessions_router
from app.api.workouts import router as workout_router


app = FastAPI()

app.include_router(gym_router)
app.include_router(staff_router)
app.include_router(staff_router)
app.include_router(progress_router)
app.include_router(workout_sessions_router)
app.include_router(workout_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", reload=True)
