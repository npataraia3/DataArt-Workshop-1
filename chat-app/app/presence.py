import time

active_users = {}  # user_id -> last_active_timestamp

AFK_TIMEOUT = 60

def update_activity(user_id):
    active_users[user_id] = time.time()

def get_status(user_id):
    if user_id not in active_users:
        return "offline"

    diff = time.time() - active_users[user_id]

    if diff < AFK_TIMEOUT:
        return "online"
    return "afk"