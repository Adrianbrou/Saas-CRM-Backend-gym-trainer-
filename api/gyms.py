from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.gym import GymCreate, GymResponse, GymUpdate
from app.services import gym_service


router = APIRouter(prefix="/gyms", tags=["gyms"])


@router.post("/", response_model=GymResponse)
def create_gym(data: GymCreate, db: Session = Depends(get_db)):
    """Create a new gym. Returns 400 if a gym with the same name and location already exists."""
    try:
        return gym_service.register_gym(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[GymResponse])
def get_all_gym(db: Session = Depends(get_db)):
    """Return all gyms in the system."""
    return gym_service.get_all(db)


@router.get("/{gym_id}", response_model=GymResponse)
def get_gym_id(gym_id: int, db: Session = Depends(get_db)):
    """Return a single gym by ID. Returns 404 if not found."""
    try:
        return gym_service.get_gym(db, gym_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{gym_id}", response_model=GymResponse)
def update_gym(data: GymUpdate, gym_id: int, db: Session = Depends(get_db)):
    """Partially update a gym's fields. Returns 404 if not found."""
    try:
        return gym_service.update_gym(db, gym_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{gym_id}", response_model=bool)
def delete(gym_id: int, db: Session = Depends(get_db)):
    """Delete a gym by ID. Returns 404 if not found."""
    try:
        return gym_service.delete_gym(db, gym_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
