from fastapi import Depends, HTTPException, status,APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,HTTPBasicCredentials,HTTPBasic
from jose import jwt, JWTError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from ..core.db import get_db
from typing import Annotated
import uuid
from ..core.models import User
from fastapi import Request
from ..utils.security import hash_password,verify_password

SECRET_KEY = "0697465f108e9f58af1208bc8f3c7bf388bd5528f8a7fb9189222098472761d6"
ALGORITHM = "HS256"
security = HTTPBearer()
security_basic= HTTPBasic()
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.post("/register")
def register_user(credentials: Annotated[HTTPBasicCredentials, Depends(security_basic)], db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        if not credentials.password or not credentials.username:
            raise HTTPException(status_code=500, detail="No se proporciono Usuario o contrasena")
        hashed_password = hash_password(credentials.password)
        user = User(id=uuid.uuid4(), username=credentials.username, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}

@router.post("/login")
def login_user(credentials: Annotated[HTTPBasicCredentials, Depends(security_basic)], db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, hashed_password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}




@router.get("/me")
def user_data( db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return {
        "user_id": user_id
    }
