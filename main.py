from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import models
from app.api import auth
from app.api import auth, dependents
from app.api import auth, dependents, appointment_types


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Agendamento Psicopedagógico",
    description="API Backend com FastAPI, PostgreSQL e Google Calendar API",
    version="1.0.0"
)

# A inclusão do router tem de estar aqui
app.include_router(auth.router)
app.include_router(dependents.router)
app.include_router(appointment_types.router)

@app.get("/")
def root():
    return {"status": "online", "message": "API de Agendamento Psicopedagógico rodando com sucesso!"}

