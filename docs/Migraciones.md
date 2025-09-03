# Correr Migraciones

1. alembic revision --autogenerate -m "Create users table"
2. Revisar que se creen las migraciones correspodientes en /alembic/versions
3. alembic upgrade head