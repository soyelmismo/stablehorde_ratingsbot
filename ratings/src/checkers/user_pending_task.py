from ..config import db
def check(user_id):
    if db.get_attributes_dict(user_id, ["pending"]) == "True":
        return True
    return False
