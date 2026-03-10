from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.gym import GymCreate, GymResponse
from app.services import gym_service


router = APIRouter(prefix="/gyms", tags=["gyms"])


@router.post("/", response_model=GymResponse)
def create_gym(data: GymCreate, db: Session = Depends(get_db)):
    return gym_service.register_gym(db, data)


@router.get("/", response_model=list[GymResponse])
def get_all_gym(db: Session = Depends(get_db)):
    return gym_service.get_all(db)


@router.get("/{gym_id}", response_model=GymResponse)
def get_gym_id(gym_id: int, db: Session = Depends(get_db)):
    return gym_service.get_gym(db, gym_id)
