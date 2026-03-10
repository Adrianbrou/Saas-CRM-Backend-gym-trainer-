from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.gym import GymCreate, GymResponse
from app.services import gym_service


router = APIRouter(prefix="/gyms", tags=["gyms"])


@router.post("/", response_model=GymResponse)
def create_gym(data: GymCreate, db: Session = Depends(get_db)):
    return gym_service.register_gym(db, data)
