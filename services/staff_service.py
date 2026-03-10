"""
staff_service.py — Business Logic for Staff

Staff are tenant-scoped: each staff member belongs to a gym via gym_id.
Email must be unique per gym — two staff at different gyms can share an email,
but not two staff at the same gym.
"""

from app.models.staff import Staff
from app.repository import staff_repository
from app.schemas.staff import StaffCreate, StaffUpdate
from sqlalchemy.orm import Session


def register_staff(db: Session, data: StaffCreate) -> Staff:
    """Register a new staff member after verifying the email is not already taken in this gym.

    Args:
        db (Session): Session to the database.
        data (StaffCreate): Validated schema containing role, name, email, phone, gym_id.

    Raises:
        ValueError: If a staff member with the same email already exists in this gym.

    Returns:
        Staff: The newly created staff member with database-generated id and timestamps.
    """
    existing = staff_repository.get_by_email(db, data.email, data.gym_id)
    if existing:
        raise ValueError("Staff member already exists in this gym")
    staff = Staff(**data.model_dump())
    return staff_repository.create(db, staff)


def update_staff(db: Session, staff_id: int, data: StaffUpdate) -> Staff:
    """Update an existing staff member's fields after verifying they exist.

    Args:
        db (Session): Session to the database.
        staff_id (int): Primary key of the staff member to update.
        data (StaffUpdate): Validated schema — all fields optional.

    Raises:
        ValueError: If no staff member with that id exists.

    Returns:
        Staff: The updated staff member with new values reflected.
    """
    existing = staff_repository.get_by_id(db, staff_id)
    if not existing:
        raise ValueError("Staff not found")
    updates = data.model_dump(exclude_unset=True)
    return staff_repository.update(db, staff_id, updates)


def get_staff(db: Session, staff_id: int) -> Staff:
    """Retrieve a staff member by id after verifying they exist.

    Args:
        db (Session): Session to the database.
        staff_id (int): Primary key of the staff member to retrieve.

    Raises:
        ValueError: If no staff member with that id exists.

    Returns:
        Staff: The matching staff member object.
    """
    existing = staff_repository.get_by_id(db, staff_id)
    if not existing:
        raise ValueError("Staff not found")
    return existing


def delete_staff(db: Session, staff_id: int) -> bool:
    """Delete a staff member after verifying they exist.

    Args:
        db (Session): Session to the database.
        staff_id (int): Primary key of the staff member to delete.

    Raises:
        ValueError: If no staff member with that id exists.

    Returns:
        bool: True if the staff member was found and deleted.
    """
    existing = staff_repository.get_by_id(db, staff_id)
    if not existing:
        raise ValueError("Staff not found")
    staff_repository.delete(db, staff_id)
    return True
