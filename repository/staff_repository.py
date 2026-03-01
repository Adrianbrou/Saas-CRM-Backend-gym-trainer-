from sqlalchemy.orm import Session
from app.models.staff import Staff
from typing import List


def create(db: Session, staff: Staff) -> Staff:
    """Insert a new staff member into the database.

    Args:
        db (Session): Database session injected from outside — never created here.
        staff (Staff): A Staff model instance built by the service layer.

    Returns:
        Staff: The created staff member with generated id, created_at, etc. loaded from DB.
    """
    db.add(staff)
    db.commit()
    db.refresh(staff)

    return staff


def get_by_id(db: Session, staff_id: int) -> Staff | None:
    """Fetch a single staff member by their id.

    Args:
        db (Session): Database session injected from outside.
        staff_id (int): The id of the staff member to look up.

    Returns:
        Staff | None: The staff member if found, None if no staff with that id exists.
    """
    return db.query(Staff).filter(Staff.id == staff_id).first()


def get_all(db: Session, gym_id: int) -> List[Staff]:
    """Fetch all staff members belonging to a specific gym.

    Filters by gym_id to enforce multi-tenant isolation —
    a gym must never see another gym's staff.

    Args:
        db (Session): Database session injected from outside.
        gym_id (int): The id of the gym whose staff to retrieve.

    Returns:
        List[Staff]: All staff registered under that gym. Empty list if none.
    """
    return db.query(Staff).filter(Staff.gym_id == gym_id).all()


def get_by_email(db: Session, email: str, gym_id: int) -> Staff | None:
    """Fetch a staff member by email within a specific gym.

    Used by the service layer to check for duplicate emails before creating
    a new staff member. Email uniqueness is per gym.

    Args:
        db (Session): Database session injected from outside.
        email (str): The email address to search for.
        gym_id (int): The gym to search within (tenant isolation).

    Returns:
        Staff | None: The staff member if found, None if no match.
    """
    return db.query(Staff).filter(Staff.email == email, Staff.gym_id == gym_id).first()


def update(db: Session, staff_id: int, updates: dict) -> Staff | None:
    """Update an existing staff member's fields using a dictionary of changes.

    Fetches the staff member by id, then loops over the updates dict and applies
    each field dynamically using setattr(staff, key, value). Only fields
    present in the dict are changed; everything else stays the same.

    Args:
        db (Session): Database session injected from outside.
        staff_id (int): The id of the staff member to update.
        updates (dict): Fields to update e.g. {"name": "Alice", "role": "manager"}

    Returns:
        Staff | None: The updated staff member, or None if no staff with that id exists.
    """
    staff = get_by_id(db, staff_id)
    if not staff:
        return None
    for key, value in updates.items():
        setattr(staff, key, value)
    db.commit()
    db.refresh(staff)

    return staff


def delete(db: Session, staff_id: int) -> bool:
    """Delete a staff member from the database by their id.

    Fetches the staff object first — db.delete() requires the object,
    not the id. Returns False immediately if the staff member does not exist.

    Args:
        db (Session): Database session injected from outside.
        staff_id (int): The id of the staff member to delete.

    Returns:
        bool: True if deleted successfully, False if no staff with that id exists.
    """
    staff = get_by_id(db, staff_id)
    if not staff:
        return False
    db.delete(staff)
    db.commit()

    return True
