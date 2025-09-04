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


## Extras
1. Se crearon actions para probar la BD de postgres y Nuestra app , ademas se ejecutan los test automaticos cada vez que se hace un pull y se migra automaticamente 
2. Para Saber sobre los Test referirse a la [Documentacion](/docs/Tests.md)
3. Para Saber mas sobre como se abordo las problematicas referirse a la [Documentacion](/docs/Problematicas.md)
4. Para saber mas sobre como se implemento el CI/CD referirse a la [Documentacion](/docs/Workflows.md)