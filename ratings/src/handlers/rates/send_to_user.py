from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from ...config import db, emojis_artifacts, emojis_rating

from .new import request
from .tools.get_image import download
from .tools.reset_user_rate_data import run as reset_data

caption = f"Rate this image:\n\n Good-looking? - (1: Horrible | 10: Excellent)\nBad details - ({emojis_artifacts[4]}: A lot! | {emojis_artifacts[0]}: No)"

keyboard = [
        [InlineKeyboardButton(emojis_rating[i], callback_data='calif|rating|%d' % (i+1)) for i in range(5)],
        [InlineKeyboardButton(emojis_rating[i+5], callback_data='calif|rating|%d' % (i+6)) for i in range(5)],
        [InlineKeyboardButton(emojis_artifacts[4-i], callback_data='calif|artifacts|%d' % (5-i)) for i in range(5)]
]

async def handle(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    user_data = db.get(user_id)
    if user_data is None:
        db.set(user_id, {})
    else:
        await reset_data(user_id)

    resp = await request()
    image_id = resp["id"]


    # Descarga la imagen y la guarda
    image = await download(resp["url"], image_id)

    # Enviar imagen al usuario
    image.seek(0)
    c_msg = await update.effective_chat.send_photo(photo=image, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
    image=None # Limpiar

    # Actualiza los datos del usuario
    db.set_subkey(user_id, "id", image_id)
    db.set_subkey(user_id, "c_chan", str(c_msg.chat.id))
    db.set_subkey(user_id, "c_mess", str(c_msg.message_id))
