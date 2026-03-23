from sqlalchemy import Column, Integer, String, Boolean, Text

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    token = Column(String)

class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    friend_id = Column(Integer)
    accepted = Column(Boolean, default=False)

class Ban(Base):
    __tablename__ = "bans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    banned_user_id = Column(Integer)

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    is_private = Column(Boolean)
    owner_id = Column(Integer)

class RoomMember(Base):
    __tablename__ = "room_members"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    room_id = Column(Integer)
    is_admin = Column(Boolean, default=False)

class RoomBan(Base):
    __tablename__ = "room_bans"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer)
    user_id = Column(Integer)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(Integer)
    room_id = Column(Integer, nullable=True)
    receiver_id = Column(Integer, nullable=True)
    reply_to = Column(Integer, nullable=True)
    edited = Column(Boolean, default=False)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    path = Column(String)
    room_id = Column(Integer, nullable=True)
    user_id = Column(Integer)