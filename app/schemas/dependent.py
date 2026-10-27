from pydantic import BaseModel
from typing import Optional
from datetime import date

class DependentBase(BaseModel):
    full_name: str
    birth_date: date
    notes: Optional[str] = None

class DependentCreate(DependentBase):
    pass

class DependentUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    notes: Optional[str] = None

class DependentResponse(DependentBase):
    id: int
    parent_id: int

    class Config:
        from_attributes = True