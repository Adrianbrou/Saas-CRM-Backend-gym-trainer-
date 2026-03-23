from sqlalchemy.orm import Session
from app.models.member import Member
from typing import List


def create(db: Session, member: Member) -> Member:
    """Insert a new member into the database.

    Args:
        db (Session): Database session injected from outside — never created here.
        member (Member): A Member model instance built by the service layer.

    Returns:
        Member: The created member with generated id, created_at, etc. loaded from DB.
    """
    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def get_by_id(db: Session, member_id: int) -> Member | None:
    """Fetch a single member by their id.

    Args:
        db (Session): Database session injected from outside.
        member_id (int): The id of the member to look up.

    Returns:
        Member | None: The member if found, None if no member with that id exists.
    """
    return db.query(Member).filter(Member.id == member_id).first()


def get_all(db: Session, gym_id: int, skip: int = 0, limit: int = 20) -> List[Member]:
    """Fetch all members belonging to a specific gym.

    Filters by gym_id to enforce multi-tenant isolation —
    a gym must never see another gym's members.

    Args:
        db (Session): Database session injected from outside.
        gym_id (int): The id of the gym whose members to retrieve.
        skip (int): Number of records to skip (offset). Defaults to 0.
        limit (int): Maximum number of records to return. Defaults to 20.

    Returns:
        List[Member]: All members registered under that gym. Empty list if none.
    """
    return db.query(Member).filter(Member.gym_id == gym_id).offset(skip).limit(limit).all()


def get_by_email(db: Session, email: str, gym_id: int) -> Member | None:
    """Fetch a member by email within a specific gym.

    Used by the service layer to check for duplicate emails before creating
    a new member. Email uniqueness is per gym — the same email can exist
    in two different gyms.

    Args:
        db (Session): Database session injected from outside.
        email (str): The email address to search for.
        gym_id (int): The gym to search within (tenant isolation).

    Returns:
        Member | None: The member if found, None if no match.
    """
    return db.query(Member).filter(Member.gym_id == gym_id, Member.email == email).first()


def update(db: Session, member_id: int, updates: dict) -> Member | None:
    """Update an existing member's fields using a dictionary of changes.

    Fetches the member by id, then loops over the updates dict and applies
    each field dynamically using setattr(member, key, value) — equivalent
    to member.name = value but works for any field passed as a string.
    Only fields present in the dict are changed.

    Args:
        db (Session): Database session injected from outside.
        member_id (int): The id of the member to update.
        updates (dict): Fields to update e.g. {"name": "John", "email": "j@gym.com"}

    Returns:
        Member | None: The updated member, or None if no member with that id exists.
    """
    member = get_by_id(db, member_id)
    if not member:
        return None
    for key, value in updates.items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)

    return member


def delete(db: Session, member_id: int) -> bool:
    """Delete a member from the database by their id.

    Fetches the member object first — db.delete() requires the object,
    not the id. Returns False immediately if the member does not exist.

    Args:
        db (Session): Database session injected from outside.
        member_id (int): The id of the member to delete.

    Returns:
        bool: True if deleted successfully, False if no member with that id exists.
    """
    member = get_by_id(db, member_id)
    if not member:
        return False
    db.delete(member)
    db.commit()

    return True
