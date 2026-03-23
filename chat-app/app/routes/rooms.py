from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..models import Room, RoomMember, RoomBan

router = APIRouter()

@router.post("/rooms")
def create_room(name: str, description: str, is_private: bool,
                db: Session = Depends(get_db), user=Depends(get_current_user)):

    room = Room(name=name, description=description, is_private=is_private, owner_id=user.id)
    db.add(room)
    db.commit()

    db.add(RoomMember(user_id=user.id, room_id=room.id, is_admin=True))
    db.commit()

    return room

@router.post("/rooms/{room_id}/join")
def join(room_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    ban = db.query(RoomBan).filter_by(room_id=room_id, user_id=user.id).first()
    if ban:
        return {"error": "banned"}

    db.add(RoomMember(user_id=user.id, room_id=room_id))
    db.commit()
    return {"joined": True}