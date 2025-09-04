# TESTS.

## Auth y Usuarios

* Registro exitoso y fallido (usuario existente, datos faltantes).
* Login exitoso y fallido (usuario incorrecto, contraseña incorrecta).
* Contraseña se guarda hasheada (no en texto plano).
* Acceso a endpoints protegidos con y sin token.

## CRUD de las Tareas

* Crear tarea (con y sin autenticación).
* Listar tareas (paginación, límites, offset).
* Obtener tarea por ID (existente y no existente).
* Actualizar tarea (solo del usuario autenticado).
* Eliminar tarea (solo del usuario autenticado)

## Seguridad y RateLimit

* Acceso sin token (debe fallar).
* Exceso de peticiones (debe bloquear por rate limit).
* Pruebas de CORS (solo si tienes orígenes restringidos).
------

**Para Este ejercicio se disennaron 10 test 6 fueron `Pruebas de Integracion` 2 de `Seguridad` y 2 de `BD` para un `test-coverage` del 100% en integracion**




