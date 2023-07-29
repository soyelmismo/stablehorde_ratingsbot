from ..config import db
def check(user_id):
    if db.get(user_id):
        return True
    return False
