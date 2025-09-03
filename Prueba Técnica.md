# 🧪 Prueba Técnica – Programador Backend (Python/FastAPI)

¡Gracias por tu interés en unirte a nuestro equipo! 🎉  

El objetivo es evaluar tus **habilidades prácticas**, tu **forma de organizar el código**, y tu **criterio profesional** al enfrentar situaciones reales en un entorno de backend.

---

## 🎯 Enunciado de la prueba

Crea una **API REST** usando **FastAPI** y **PostgreSQL** para administrar una lista de tareas (**TODOs**).

### Requerimientos funcionales
1. Cada tarea debe tener los siguientes campos:  [DONE]
   - `id` (UUID o entero autoincremental)  
   - `título` (string)  
   - `descripción` (string, opcional)  
   - `estado` (pendiente/completada)  
   - `fecha_creación` (timestamp)  
   - `id_usuario` (para distinguir tareas entre diferentes usuarios)  

2. La API debe exponer los siguientes endpoints:  [DONE]
   - `POST /tasks` → Crear una nueva tarea.  
   - `GET /tasks` → Listar todas las tareas del usuario autenticado.  
   - `GET /tasks/{id}` → Obtener el detalle de una tarea por su ID.  
   - `PUT /tasks/{id}` → Actualizar una tarea (estado, título o descripción).  
   - `DELETE /tasks/{id}` → Eliminar una tarea.  

3. **Autenticación básica**:  [DONE]
   - Implementar un sistema sencillo de autenticación (ejemplo: JWT o token en headers).  
   - Cada usuario solo puede acceder a sus propias tareas.  

4. **Persistencia en base de datos**: [DONE] 
   - Usa **PostgreSQL** (no SQLite).  
   - Define correctamente los modelos usando **SQLAlchemy o SQLModel**.  

---

## ⚡️ Problemáticas adicionales a considerar

La API se usará en un **entorno real**. Considera lo siguiente al diseñar tu solución:

1. **Alta concurrencia**  
   - La aplicación será utilizada por muchos usuarios al mismo tiempo.  

2. **Grandes volúmenes de datos**  
   - Algunos usuarios pueden tener cientos o miles de tareas.  

3. **Escenarios de error**  
   - Es posible que un usuario intente acceder a una tarea que no existe o envíe datos inválidos.  

4. **Seguridad**  
   - Cada usuario debe tener acceso solo a sus propias tareas.  

👉 Cómo resuelvas estos puntos dependerá de tu criterio y experiencia.  

---

## 🌟 Plus (no obligatorio, pero valorado)

- Tests automatizados.  [DONE]
- Docker Compose para levantar la API y PostgreSQL fácilmente.  [DONE]
- Logging básico para errores y auditoría.  
- Migraciones con **Alembic**.  [DONE]

---

## 📂 Entregables

- Código fuente en un repositorio público o privado (GitHub).  
- Un archivo **README.md** con:  
  - Instrucciones para correr el proyecto.  
  - Ejemplos de uso de los endpoints (puede ser con `curl` o `httpie`).  
  - Si usas Docker, incluir instrucciones claras de levantamiento.  

---

## 📝 Criterios de evaluación

Cada aspecto se evaluará en una escala de **0 a 5 puntos**:

1. **Funcionalidad (20%)**  
   - ¿Los endpoints cumplen con lo solicitado y funcionan correctamente?  

2. **Calidad del código (20%)**  
   - ¿El código está limpio, modular y bien organizado?  

3. **Resolución de problemáticas (30%)**  
   - ¿El candidato identificó y resolvió de forma adecuada los problemas de concurrencia, grandes volúmenes de datos, seguridad y manejo de errores?  

4. **Buenas prácticas (20%)**  
   - Validaciones, manejo de errores, documentación, separación de responsabilidades.  

5. **Extras / Iniciativa propia (10%)**  
   - Tests, Docker, migraciones, logging, etc.  

---

⏳ Tiempo estimado: **2–5 días**  
📩 Una vez finalizada, comparte tu repositorio y breve explicación de tu solución.  

¡Mucha suerte y esperamos ver tu talento en acción! 🚀

