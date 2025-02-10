from telegram import Update
from telegram.ext import ContextTypes
from handlers.lessons import basics, rhythm

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data
    if query == "basics":
        await basics(update, context)
    elif query == "rhythm":
        await rhythm(update, context)
