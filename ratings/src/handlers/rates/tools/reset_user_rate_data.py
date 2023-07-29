from ....config import db

async def run(user_id):
    db.set_subkey(user_id, "id", None)
    db.set_subkey(user_id, "rating", None)
    db.set_subkey(user_id, "artifacts", None)