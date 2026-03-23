from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Session as UserSession
from ..dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sessions = db.query(UserSession).filter_by(user_id=user.id).all()
    return sessions


@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    session = db.query(UserSession).get(session_id)

    if session and session.user_id == user.id:
        db.delete(session)
        db.commit()

    return {"message": "Session removed"}