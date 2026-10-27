from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Base comum para campos
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None

 # criar um novo usuário
class UserCreate(UserBase): # herda as variaveis da classe UserBase
    password: str 

# atualizar os dados do usuário
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

# o que a API devolve ao cliente
class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Permite conversão direta dos modelos do SQLAlchemy

#Dados que a API retorna para o cliente sobre login e Token JWT)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None