from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Friend

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/friends/request")
def send_request(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    f = Friend(user_id=user_id, friend_id=friend_id)
    db.add(f)
    db.commit()
    return {"message": "Request sent"}

@router.post("/friends/accept")
def accept_request(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    f = db.query(Friend).filter_by(user_id=friend_id, friend_id=user_id).first()
    if f:
        f.accepted = True
        db.commit()
    return {"message": "Accepted"}