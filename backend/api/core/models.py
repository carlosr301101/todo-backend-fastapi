from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from .db import Base

class TaskStatus(enum.Enum):
    pendiente = "pendiente"
    completada = "completada"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(Enum(TaskStatus), default=TaskStatus.pendiente, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)



class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)