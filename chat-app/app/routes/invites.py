from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import RoomMember, Room
from ..dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/rooms/{room_id}/invite")
def invite_user(room_id: int, user_id: int,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):

    room = db.query(Room).get(room_id)

    if not room:
        raise HTTPException(404, "Room not found")

    if not room.is_private:
        raise HTTPException(400, "Invites only for private rooms")

    # Only owner/admin can invite
    member = db.query(RoomMember).filter_by(
        room_id=room_id,
        user_id=current_user.id
    ).first()

    if not member or not member.is_admin:
        raise HTTPException(403, "Not allowed")

    db.add(RoomMember(user_id=user_id, room_id=room_id))
    db.commit()

    return {"message": "User invited"}