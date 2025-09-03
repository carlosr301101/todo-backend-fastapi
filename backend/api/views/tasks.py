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

router = APIRouter()


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

@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
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

@router.get("/tasks", response_model=PaginatedTasks)
async def list_tasks(request: Request, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
                     #Aqui se declara el paginado y el offset
                     limit:int=3,
                     offset:int=2
                     ):
    try:
        total = db.query(Task).filter(Task.id_usuario == user_id).count()
        tasks = (
            db.query(Task)
            .filter(Task.id_usuario == user_id)
            .order_by(Task.fecha_creacion.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
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