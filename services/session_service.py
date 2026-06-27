import time
from config import SESSION_TIMEOUT

user_sessions = {}

def get_session(user_id):
    current_time = time.time()

    if user_id not in user_sessions or \
       current_time - user_sessions[user_id]["last_active"] > SESSION_TIMEOUT:
        user_sessions[user_id] = {
            "intent": None,
            "order_id": None,
            "chat_history": []
        }

    user_sessions[user_id]["last_active"] = current_time
    return user_sessions[user_id]