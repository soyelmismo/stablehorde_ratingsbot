from aiohttp import ClientSession
from json import loads

from telegram import Update
from telegram.ext import CallbackContext

from ..config import headers

async def check(update: Update, context: CallbackContext):
    async with ClientSession() as session:
        resp = await session.get('https://stablehorde.net/api/v2/find_user', headers=headers)
        data = await resp.read()
        data = loads(data.decode('utf-8'))

    coins = int(abs(data["kudos_details"].get("accumulated")))
    await update.effective_chat.send_message(text=f'Total collected coins: {coins}', reply_to_message_id=update.effective_message.message_id)
