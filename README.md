# Inicializar el Backend
0. `git clone` este repo

1. Instalar uv para windowns `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` o usar `curl -LsSf https://astral.sh/uv/install.sh | sh` en linux y macOS

2. Una vez instalado `uv` desde la raiz del proyecto hacemos `uv sync` para instalar las dependencias de nuestro programa.

3. Terminado de instalar hacemos `uv run uvicorn backend.api.app::app --workers 4` Desde la raiz del proyecto. 

## Enfoque Optado en la construccion de la tarea

* En este caso se ha optado por un enfoque de usar nuestro backend en varios hilos pra poder compartimentar la carga de trabajo y eliminar las demoras innecesarias.

* Al registrarse en la app con el endpoint `/auth/register` poniendo el usuario y contrasena devuelve un Token de Auth ademas el password se guarda hasheado en la BD.

* Se uso funciones asincronas en la confeccion de los endpoints que mas solicitudes se esperan que tengan, para evitar las funciones bloqueantes.

* Se hizo un filtrado e indexado de la BD de Postgres para optimizar las query en las tablas y obtener un mejor performance de nuestra BD como se puede apreciar. LAs tareas son mostradas por fecha de creacion

```py
@router.get("/tasks/{id}", response_model=TaskOut)
async def get_task(id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == id, Task.id_usuario == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task
```

* Se implemento un paginado para poder manejar grandes volumenes de datos por parte del usuario. Como se puede apreciar

```py
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
        

```


* Se implemento un throttle para EVITAR tareas de automatizacion y sobrecargas innecesarias a nuestro backend.
```py
##`POST /tasks`
@limiter.limit("10/minute")# Evita Bots en la creacion de tareas y tenemos un mejor trafico ya que bloquea entradas por ip a 10*min
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
```