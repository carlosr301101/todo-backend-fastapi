from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .core.models import Item
from .core.db import get_db
from .views.tasks import router as tasks_router
from .views.auth import create_access_token,get_current_user_id
from .core.models import User
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import uuid
import logging
security = HTTPBasic()

app = FastAPI(
    title="Todo Technical Assestment",
    description="API Todos",
    version="0.1.0",
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#####Aqui se incluyen las view del endpoint /task
app.include_router(tasks_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/login")
def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        # Crea el usuario con un id UUID y password dummy
        user = User(id=uuid.uuid4(), username=credentials.username, hashed_password=credentials.password)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}



@app.get("/me")
def user_data( db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return {
        "user_id": user_id
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 