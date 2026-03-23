from fastapi import Depends, HTTPException
from jose import jwt
from .database import SessionLocal
from .models import User

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).get(payload["user_id"])
        return user
    except:
        raise HTTPException(401, "Invalid token")