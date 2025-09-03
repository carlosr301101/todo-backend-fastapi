from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel,field_validator,validator
from typing import List, Optional
from ..core.models import Task
from ..core.db import get_db
from datetime import datetime
from ..views.auth import get_current_user_id
from uuid import UUID
from enum import Enum
from fastapi import Request
from slowapi.util import get_remote_address
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    completada = "completada"
class TaskCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None

class TaskUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[EstadoTarea] = None
    estado: Optional[EstadoTarea] = None


class TaskOut(BaseModel):
    id: UUID
    titulo: str
    descripcion: Optional[str]
    estado: EstadoTarea
    fecha_creacion: datetime
    id_usuario: UUID

    class Config:
        orm_mode = True

class PaginatedTasks(BaseModel):
    total: int
    limit: int
    offset: int
    next: Optional[str]
    previous: Optional[str]
    items: List[TaskOut]


##`POST /tasks`
# Evita Bots en la creacion de tareas y tenemos un mejor trafico ya que bloquea entradas
@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute",error_message="Demasiadas solicitudes, por favor intente de nuevo más tarde.")
def create_task(request: Request,task: TaskCreate, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    if task.descripcion is None:
        task.descripcion = "Esta descripcion es generica"
    try:
        db_task = Task(
            titulo=task.titulo,
            descripcion=task.descripcion,
            estado=EstadoTarea.pendiente,
            fecha_creacion=datetime.utcnow(),
            id_usuario=user_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la tarea: {e}")
    return db_task

# `GET /tasks` con paginación, se implemento el rate limit para que no se sobrecargue innecesariamente la app
#Nota mental el offset tiene que ser menor que la cantidad de tareas que tenga el usuario, por defecto tiene que ser 0.

@router.get("/tasks", response_model=PaginatedTasks)
@limiter.limit("15/minute")# limite a las llamadas por usuario por ip a solo 15 * min
async def list_tasks(request: Request, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id),
                     #Aqui se declara el paginado y el offset
                     limit:int=5,
                     offset:int=0
                     ):
    try:
        total = db.query(Task).filter(Task.id_usuario == user_id).count()
        tasks = db.query(Task).filter(Task.id_usuario == user_id).order_by(Task.fecha_creacion.desc()).offset(offset).limit(limit).all()
        #Con esta simple conversion nos evitamos errores de que el off set sea mayor que el total
        if offset>total:
            offset=0
            
        if not tasks:
            raise HTTPException(status_code=404, detail="No se encontraron tareas para este usuario")
        base_url = str(request.url).split("?")[0]
        next_offset = offset + limit
        prev_offset = max(offset - limit, 0)

        next_link = (
            f"{base_url}?limit={limit}&offset={next_offset}" if next_offset < total else None
        )
        prev_link = (
            f"{base_url}?limit={limit}&offset={prev_offset}" if offset > 0 else None
        )
        return PaginatedTasks(
        total=total,
        limit=limit,
        offset=offset,
        next=next_link,
        previous=prev_link,
        items=[TaskOut.model_validate(task, from_attributes=True) for task in tasks]
    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ver las tareas: {e}")
        


@router.get("/tasks/{id}", response_model=TaskOut)
async def get_task(id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == id, Task.id_usuario == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@router.put("/tasks/{id}", response_model=TaskOut)
def update_task(id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == id, Task.id_usuario == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == id, Task.id_usuario == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(task)
    db.commit()
    return