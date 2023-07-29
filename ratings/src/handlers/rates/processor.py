from asyncio import create_task
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from ...config import db
from ...checkers.in_database import check as in_database
from ...checkers.user_pending_task import check as is_pending
from .submit import send_rating
from .send_to_user import handle as rate, keyboard

db_query = ["rating", "artifacts", "id", "c_chan", "c_mess", "pending"]

async def handle(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    query = update.callback_query
    await query.answer()
    if not in_database(user_id) or is_pending(user_id): return
    call_type, rating_type, value = query.data.split('|')
    if call_type == "calif":
        db.set_subkey(user_id, rating_type, value)

        db_query = ["rating", "artifacts", "id", "c_chan", "c_mess"]
        data = db.get_attributes_dict(user_id, db_query)
        r, a = data["rating"], data["artifacts"]

        # Usamos deepcopy para obtener una copia de la lista y no modificar la original.
        from copy import deepcopy
        updated_keyboard = deepcopy(keyboard)

        # Actualizando botones
        for i, row in enumerate(updated_keyboard):
            for j, button in enumerate(row):
                # Marcamos los botones seleccionados con un 'check' si su índice coincide con el guardado en la db
                if (button.callback_data == f'calif|rating|{r}' or button.callback_data == f'calif|artifacts|{a}')  and button.text[0] != "✅":
                    updated_keyboard[i][j] = InlineKeyboardButton(text=f"✅ {button.text}", callback_data=button.callback_data)

        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, 
                                            message_id=query.message.message_id, 
                                            reply_markup=InlineKeyboardMarkup(updated_keyboard))


        if r and a:
            db.set_subkey(user_id, "pending", "True")
            id = data["id"]
            msg_chat = data["c_chan"]
            msg_id = data["c_mess"]
            create_task(rate(update, context))
            create_task(send_rating(context, r, a, id, msg_chat, msg_id, user_id))
