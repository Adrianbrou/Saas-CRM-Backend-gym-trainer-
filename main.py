from fastapi import FastAPI
from app.api.gym import router as gym_router


app = FastAPI()

app.include_router(gym_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", reload=True)
