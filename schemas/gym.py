"""
gym.py — Pydantic Schemas for Gym

=============================================================
WHAT IS PYDANTIC?
=============================================================
Pydantic is a data validation library. It lets you define
the exact shape of data coming IN to your API and going OUT
from your API using Python classes with type annotations.

When a request arrives, FastAPI automatically uses your
Pydantic schema to:
  - Validate the incoming data (correct types, required fields)
  - Return a clear error to the client if data is invalid
  - Parse the data into a Python object you can work with

=============================================================
THE THREE SCHEMA TYPES (pattern used throughout this project)
=============================================================

  GymCreate   — Data the CLIENT sends when CREATING a record.
                Only fields the client should provide.
                All fields are required.

  GymUpdate   — Data the CLIENT sends when UPDATING a record.
                Same fields as Create, but ALL are optional.
                The client only sends what they want to change.
                Optional fields are written as: field: str | None = None

  GymResponse — Data the API sends BACK to the client.
                Includes everything: id, timestamps, all fields.
                Must have: model_config = {"from_attributes": True}
                This setting allows Pydantic to read SQLAlchemy
                model instances directly (ORM mode).

=============================================================
IMPORTANT RULES
=============================================================
  - SQLAlchemy model  = database structure (tables, columns)
  - Pydantic schema   = API contract (what goes in / comes out)
  - NEVER expose raw SQLAlchemy objects to the client directly
  - model_config is only needed on Response schemas
  - Field names in Response MUST exactly match the SQLAlchemy
    model attribute names (e.g. updated_at not update_at)

=============================================================
EXAMPLE USAGE
=============================================================

  # CREATE — client sends JSON body, FastAPI validates it:
  # POST /gyms
  # Body: { "name": "FitZone", "location": "New York" }
  #
  # In the route:
  #   def create_gym(data: GymCreate, db: Session):
  #       gym = Gym(name=data.name, location=data.location)
  #       ...

  # UPDATE — client sends only what changed:
  # PATCH /gyms/1
  # Body: { "location": "Los Angeles" }   ← name not required
  #
  # In the route:
  #   def update_gym(gym_id: int, data: GymUpdate, db: Session):
  #       updates = data.model_dump(exclude_unset=True)
  #       ...

  # RESPONSE — API returns a full GymResponse object:
  # FastAPI serializes the SQLAlchemy Gym instance automatically
  # because of model_config = {"from_attributes": True}
  #
  #   def create_gym(...) -> GymResponse:
  #       ...
  #       return gym   ← Pydantic reads the SQLAlchemy object

=============================================================
"""

from pydantic import BaseModel
from datetime import datetime


class GymCreate(BaseModel):
    name: str
    location: str


class GymUpdate(BaseModel):
    name: str | None = None
    location: str | None = None


class GymResponse(BaseModel):
    id: int
    name: str
    location: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
