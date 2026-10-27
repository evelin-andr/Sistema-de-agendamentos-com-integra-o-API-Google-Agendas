from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    # Relações
    dependents = relationship("Dependent", back_populates="parent", cascade="all, delete-orphan")
    personal_appointments = relationship("Appointment", foreign_keys="[Appointment.user_id]", back_populates="client", cascade="all, delete-orphan")


class Dependent(Base):
    __tablename__ = "dependents"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relações
    parent = relationship("User", back_populates="dependents")
    appointments = relationship("Appointment", foreign_keys="[Appointment.dependent_id]", back_populates="dependent", cascade="all, delete-orphan")


class AppointmentType(Base):
    __tablename__ = "appointment_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=True)

    # Relações
    appointments = relationship("Appointment", back_populates="appointment_type")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    dependent_id = Column(Integer, ForeignKey("dependents.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    appointment_type_id = Column(Integer, ForeignKey("appointment_types.id"), nullable=False)
    date_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="agendado")  # ex: agendado, concluido, cancelado
    notes = Column(Text, nullable=True)

    # Relações explícitas
    dependent = relationship("Dependent", foreign_keys=[dependent_id], back_populates="appointments")
    client = relationship("User", foreign_keys=[user_id], back_populates="personal_appointments")
    appointment_type = relationship("AppointmentType", back_populates="appointments")