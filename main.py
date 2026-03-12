from fastapi import FastAPI
from app.api.gyms import router as gym_router
from app.api.staff import router as staff_router


app = FastAPI()

app.include_router(gym_router)
app.include_router(staff_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", reload=True)
