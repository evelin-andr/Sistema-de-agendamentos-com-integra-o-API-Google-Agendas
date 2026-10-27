from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

class AppointmentBase(BaseModel):
    dependent_id: Optional[int] = None
    user_id: Optional[int] = None
    appointment_type_id: int
    date_time: datetime
    notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_target(self) -> "AppointmentBase":
        if not self.dependent_id and not self.user_id:
            raise ValueError("O agendamento deve ser para um dependente ou para o próprio utilizador.")
        if self.dependent_id and self.user_id:
            raise ValueError("O agendamento não pode ser para o dependente e para o utilizador em simultâneo.")
        return self

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    date_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True