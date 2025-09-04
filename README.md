# Inicializar el Backend


## Inicializar el repo en Local
0. `git clone` este repo

1. Instalar uv para windowns `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` o usar `curl -LsSf https://astral.sh/uv/install.sh | sh` en linux y macOS

2. Una vez instalado `uv` desde la raiz del proyecto hacemos `uv sync` para instalar las dependencias de nuestro programa.
------
**Para el siguiente paso necesita tener una conexion a postgres local, con usuario:`todo_user` pass:`todo_pass` y haber creado una nueva tabla llamada `todo_db`:**

3. Desde la `/backend` cambiar dentro de `alembic.ini` la linea `sqlalchemy.url = postgresql://todo_user:todo_pass@db:5432/todo_db` por `sqlalchemy.url = postgresql://todo_user:todo_pass@localhost:5432/todo_db` ejecutar las migraciones con alembic usar `alembic upgrade head`

3. Terminado de instalar hacemos `uv run uvicorn backend.api.app::app --workers 4` Desde la raiz del proyecto.

4. Usar algun cliente de Api como `Postman`, `Thunder Client`, o ir a `http://127.0.0.1:8000/docs#/` desde el navegador.

------
## Iniciar app usando Docker
0. `git clone` este repo

1. Tener Docker Instalado en caso de Windown `Docker Desktop` en caso de Linux/MacOS el Daemon de `Dockerd`

2. Desde la raiz en Linux/MacOS hacer `docker compose up --build` o en Windown Iniciar Docker Desktop.


## Ejemplos de uso
1. Registro y Usuarios
```bash
#Registrarse
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tu_usuario",
    "password": "tu_contraseña"
  }'

# Iniciar sesión y obtener token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tu_usuario",
    "password": "tu_contraseña"
  }'
#Esto te devuelve un Token y un user ID
```
-----
**Se debe guardar el Token en una variable de entorno o en algun lugar `export TOKEN="tu_token_jwt_aqui"`**
2. CRUD de tasks
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Mi primera tarea",
    "descripcion": "Esta es una descripción opcional"
  }'
```
-----
**Obtener tareas con su paginacion**

NOTESE QUE LAS TAREAS VIENEN CON SU UUID y como tal este es el parametro que se necesita enviar en el [PUT,DELETE] y `tasks/uuid`.
```bash
# Listar primeras 5 tareas
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/tasks?limit=5&offset=0"

# Listar siguientes 5 tareas
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/tasks?limit=5&offset=5"
```
-----
**Obtener tarea especifica**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/tasks/123e4567-e89b-12d3-a456-426614174000"
```
-----
**Actualizar Tarea**
```bash
curl -X PUT "http://localhost:8000/tasks/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Título actualizado",
    "estado": "completada"
  }'
```
-----
**Eliminar Tarea**
```bash
curl -X DELETE "http://localhost:8000/tasks/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer $TOKEN"
```

## Extras
1. Se crearon actions para probar la BD de postgres y Nuestra app , ademas se ejecutan los test automaticos cada vez que se hace un pull y se migra automaticamente 
2. Para Saber sobre los Test referirse a la [Documentacion](/docs/Tests.md)
3. Para Saber mas sobre como se abordo las problematicas referirse a la [Documentacion](/docs/Problematicas.md)
4. Para saber mas sobre como se implemento el CI/CD referirse a la [Documentacion](/docs/Workflows.md)