from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..models import Message

router = APIRouter()

@router.post("/messages")
def send_message(content: str, room_id: int = None, receiver_id: int = None, reply_to: int = None,
                 db: Session = Depends(get_db), user=Depends(get_current_user)):

    msg = Message(
        content=content,
        user_id=user.id,
        room_id=room_id,
        receiver_id=receiver_id,
        reply_to=reply_to
    )
    db.add(msg)
    db.commit()
    return msg

@router.put("/messages/{id}")
def edit_message(id: int, content: str, db=Depends(get_db), user=Depends(get_current_user)):
    msg = db.query(Message).get(id)
    if msg.user_id == user.id:
        msg.content = content
        msg.edited = True
        db.commit()
    return msg

@router.delete("/messages/{id}")
def delete_message(id: int, db=Depends(get_db), user=Depends(get_current_user)):
    msg = db.query(Message).get(id)
    if msg.user_id == user.id:
        db.delete(msg)
        db.commit()
    return {"deleted": True}