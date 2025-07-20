# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import usuario as usuario_router
from app.routers import auth as auth_router
from app.routers import inventario as inventario_router
from app.models.database import create_db_and_tables


# --- Ciclo de vida de la aplicación (Opcional) ---
# Puedes usar lifespan para tareas de inicio/apagado, como crear tablas
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicación y base de datos...")
    await create_db_and_tables()  # Descomentar para crear tablas al inicio
    print("Base de datos lista.")
    yield  # La aplicación se ejecuta aquí
    print("Cerrando aplicación...")


# Crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Inventarios Coco Salvaje",
    description="API para gestionar el inventario de Coco Salvaje.",
    version="1.0.0",
    lifespan=lifespan,  # Usa el contexto de vida para crear tablas
)

# Incluye el router de usuarios en la aplicación principal
app.include_router(usuario_router.router)
# Incluye el router de autenticación en la aplicación principal
app.include_router(auth_router.router)
# Incluye el router de elementos de inventario
app.include_router(inventario_router.router)


# Ruta raíz simple para verificar que la API está funcionando
@app.get("/", tags=["Root"])
async def read_root():
    """Ruta raíz de la API."""
    return {"message": "Bienvenido a la API de Gestión de Citas"}


# --- Instrucciones para Ejecutar (en comentario) ---
# 1. Asegúrate de tener PostgreSQL corriendo y la base de datos creada.
# 2. Configura la variable de entorno DATABASE_URL (en .env o directamente).
#    Ejemplo: export DATABASE_URL="postgresql+psycopg://user:password@host:port/db"
# 3. Ejecuta el servidor con Uvicorn:
#    uvicorn main:app --reload --host 0.0.0.0 --port 8000
#    --reload: Recarga automáticamente al detectar cambios en el código.
#    --host 0.0.0.0: Hace accesible la API desde otras máquinas en la red.
#    --port 8000: Puerto en el que correrá la API.
# 4. Accede a la documentación interactiva en: http://localhost:8000/docs
