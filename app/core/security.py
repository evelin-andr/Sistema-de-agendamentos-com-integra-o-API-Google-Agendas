from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  # senha de assinatura do servidor
if not SECRET_KEY:
    raise ValueError("ERRO: A variável SECRET_KEY não foi configurada no arquivo .env!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")  # método de assinatura
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # tempo que um token de login dura

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # cria a ferramenta do hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verifica se a senha que o usuário digitou está de acordo com a do banco
    # Alterado para 72 (limite máximo do Bcrypt)
    safe_password = plain_password[:72]
    return pwd_context.verify(safe_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Transforma as senhas em hash
    # Alterado para 72 e corrigido o retorno para usar a variável safe_password
    safe_password = password[:72]
    return pwd_context.hash(safe_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um novo token JWT de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
