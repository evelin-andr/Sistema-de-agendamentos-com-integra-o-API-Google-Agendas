from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import User, AppointmentType
from app.schemas.appointment_type import AppointmentTypeCreate, AppointmentTypeResponse

router = APIRouter(prefix="/appointment-types", tags=["Tipos de Consulta"])

@router.post("/", response_model=AppointmentTypeResponse, status_code=status.HTTP_201_CREATED)
def create_appointment_type(
    type_data: AppointmentTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria um novo tipo de consulta (Exclusivo para administradores)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar tipos de consulta."
        )
    
    new_type = AppointmentType(
        name=type_data.name,
        description=type_data.description,
        duration_minutes=type_data.duration_minutes,
        price=type_data.price
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type

@router.get("/", response_model=List[AppointmentTypeResponse])
def list_appointment_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos os tipos de consulta disponíveis para agendamento."""
    return db.query(AppointmentType).all()