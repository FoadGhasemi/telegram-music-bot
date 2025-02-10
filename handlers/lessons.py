from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
import asyncio

logger = logging.getLogger(__name__)

# Lesson menu
def lesson_menu():
    keyboard = [
        [InlineKeyboardButton("Basics", callback_data="basics")],
        [InlineKeyboardButton("Rhythm", callback_data="rhythm")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Basics lesson
async def basics(update: Update, context):
    # Similar to your current implementation
    pass

# Rhythm lesson
async def rhythm(update: Update, context):
    # Similar to your current implementation
    pass
