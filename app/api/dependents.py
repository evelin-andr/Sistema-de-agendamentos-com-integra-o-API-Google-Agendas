from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import User, Dependent
from app.schemas.dependent import DependentCreate, DependentResponse, DependentUpdate

router = APIRouter(prefix="/dependents", tags=["Dependentes"])

@router.post("/", response_model=DependentResponse, status_code=status.HTTP_201_CREATED)
def create_dependent(
    dependent_data: DependentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Regista um novo dependente associado ao utilizador autenticado."""
    new_dependent = Dependent(
        full_name=dependent_data.full_name,
        birth_date=dependent_data.birth_date,
        notes=dependent_data.notes,
        parent_id=current_user.id
    )
    db.add(new_dependent)
    db.commit()
    db.refresh(new_dependent)
    return new_dependent

@router.get("/", response_model=List[DependentResponse])
def list_user_dependents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos os dependentes do utilizador autenticado."""
    dependents = db.query(Dependent).filter(Dependent.parent_id == current_user.id).all()
    return dependents