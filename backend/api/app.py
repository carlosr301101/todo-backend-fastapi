from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .core.models import Item
from .core.db import get_db
from .views.tasks import router as tasks_router
from .views.auth import router as auth_router
from .views.auth import create_access_token,get_current_user_id

from fastapi.security import HTTPBasic, HTTPBasicCredentials

import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


security = HTTPBasic()

app = FastAPI(
    title="Todo Technical Assestment",
    description="API Todos",
    version="0.1.0",
    
)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#####Aqui se incluyen las view del endpoint /task y /auth
app.include_router(tasks_router,prefix="/api")
app.include_router(auth_router,prefix="/auth")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 