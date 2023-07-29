from json import loads
from aiohttp import ClientSession

from telegram.ext import CallbackContext

from ...config import base_url, headers, db


async def send_rating(context: CallbackContext, r, a, id, msg_chat, msg_id, user_id):

    payload = {"rating": int(r), "artifacts": int(a)}
    async with ClientSession() as session:
        resp = await session.post(f'{base_url}/{id}', json=payload, headers=headers)
        data = await resp.read()
        text = loads(data.decode('utf-8'))

    winwin = text.get("reward")
    if winwin:
        text = f"Rated: {r} / {a}\n\nWe earned {winwin} poins!"
    else:
        text = "Error :("
    db.set_subkey(user_id, "pending", "False")
    await context.bot.edit_message_caption(caption=text, chat_id=msg_chat, message_id=msg_id, reply_markup=None)
