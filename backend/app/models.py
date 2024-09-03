import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

class Match(SQLModel):
    home_team: str
    away_team: str
