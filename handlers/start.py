from telegram import Update
from telegram.ext import ContextTypes
from handlers.lessons import lesson_menu  # Import the lesson menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Welcome to the Music Theory Bot.\n"
        "Choose a topic to start learning:",
        reply_markup=lesson_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Welcome and lesson menu\n"
        "/help - Show this help message"
    )
