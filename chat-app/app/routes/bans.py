from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Ban

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ban")
def ban(user_id: int, banned_user_id: int, db: Session = Depends(get_db)):
    b = Ban(user_id=user_id, banned_user_id=banned_user_id)
    db.add(b)
    db.commit()
    return {"message": "User banned"}