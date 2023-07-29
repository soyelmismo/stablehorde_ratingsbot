import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler,
    AIORateLimiter
)

from .config import tg

from .handlers.rates.send_to_user import handle as rate
from .handlers.rates.processor import handle as rate_buttons
from .checkers.kudos import check as kudos

async def start(update: Update, context: CallbackContext):
    await rate(update, context)

async def post_init(application: Application):
    commandos = [
        ("/start", "♾️"),
        ("/rate", "🌟"),
        ("/points", "🪙")
    ]
    await application.bot.set_my_commands(commandos)

def build_application():
    return (
        ApplicationBuilder()
        .token(tg)
        .concurrent_updates(True)
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .rate_limiter(AIORateLimiter(max_retries=5))
        .post_init(post_init)
        .build()
    )

def main() -> None:
    application = build_application()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("rate", rate))
    application.add_handler(CommandHandler("points", kudos))
    application.add_handler(CallbackQueryHandler(rate_buttons, pattern="^calif"))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.run_polling())
