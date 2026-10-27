from pydantic import BaseModel
from typing import Optional

class AppointmentTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_minutes: int
    price: Optional[float] = None

class AppointmentTypeCreate(AppointmentTypeBase):
    pass

class AppointmentTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None

class AppointmentTypeResponse(AppointmentTypeBase):
    id: int

    class Config:
        from_attributes = True