from fastapi import FastAPI, WebSocket
from .database import Base, engine
from .routes import users, auth, friends, rooms, messages, files, sessions, invites

app.include_router(sessions.router)
app.include_router(invites.router)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(friends.router)
app.include_router(rooms.router)
app.include_router(messages.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"status": "running"}