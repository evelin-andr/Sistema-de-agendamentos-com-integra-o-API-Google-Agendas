from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import User, Dependent, AppointmentType, Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Agendamentos"])

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria um novo agendamento para o próprio utilizador ou para um dependente."""
    
    # Se for para um dependente, verificar se ele existe e pertence ao utilizador
    if appointment_data.dependent_id:
        dependent = db.query(Dependent).filter(Dependent.id == appointment_data.dependent_id).first()
        if not dependent:
            raise HTTPException(status_code=404, detail="Dependente não encontrado.")
        if not current_user.is_admin and dependent.parent_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Não tem permissão para criar agendamentos para este dependente."
            )
            
    # Se for para o próprio utilizador, garantir que o user_id corresponde ao autenticado
    if appointment_data.user_id:
        if not current_user.is_admin and appointment_data.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Só pode criar agendamentos para si próprio."
            )
    
    # Verificar se o tipo de consulta existe
    app_type = db.query(AppointmentType).filter(AppointmentType.id == appointment_data.appointment_type_id).first()
    if not app_type:
        raise HTTPException(status_code=404, detail="Tipo de consulta não encontrado.")

    new_appointment = Appointment(
        dependent_id=appointment_data.dependent_id,
        user_id=appointment_data.user_id,
        appointment_type_id=appointment_data.appointment_type_id,
        date_time=appointment_data.date_time,
        notes=appointment_data.notes,
        status="agendado"
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.get("/", response_model=List[AppointmentResponse])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista os agendamentos do utilizador (pessoais e dos seus dependentes)."""
    if current_user.is_admin:
        return db.query(Appointment).all()
    else:
        user_dependents_ids = [d.id for d in current_user.dependents]
        return db.query(Appointment).filter(
            (Appointment.dependent_id.in_(user_dependents_ids)) | (Appointment.user_id == current_user.id)
        ).all()