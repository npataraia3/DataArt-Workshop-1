from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User, Session as UserSession
from ..auth import verify_password, hash_password, create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"user_id": user.id})

    session = UserSession(user_id=user.id, token=token)
    db.add(session)
    db.commit()

    return {"token": token}


@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):
    session = db.query(UserSession).filter_by(token=token).first()

    if session:
        db.delete(session)
        db.commit()

    return {"message": "Logged out"}


@router.post("/change-password")
def change_password(user_id: int, old_password: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if not verify_password(old_password, user.password):
        raise HTTPException(400, "Wrong password")

    user.password = hash_password(new_password)
    db.commit()

    return {"message": "Password updated"}


@router.post("/reset-password")
def reset_password(email: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(404, "User not found")

    user.password = hash_password(new_password)
    db.commit()

    return {"message": "Password reset"}