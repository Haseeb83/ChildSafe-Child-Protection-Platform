from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_jwt_secret_here")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_jwt(role: str = "user"):
    expire = datetime.utcnow() + timedelta(minutes=30)
    data = {"role": role, "exp": expire}
    return encode(data, SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        role = payload.get("role")
        if role is None:
            raise HTTPException(401, "Invalid token")
        return role
    except PyJWTError:
        raise HTTPException(401, "Invalid token")

def rbac(role: str):
    def _rbac(current_role: str = Depends(get_current_user)):
        if current_role != role:
            raise HTTPException(403, "Insufficient permissions")
        return current_role
    return _rbac

limiter = Limiter(key_func=get_remote_address)