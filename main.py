import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from handlers.start import start, help_command
from handlers.callbacks import handle_button
from utils.logging_setup import setup_logger

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure the bot token is loaded
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Please check your .env file.")

# Set up logger
logger = setup_logger()


async def main():
    """Asynchronous main function to start the bot."""
    logger.info("Starting bot...")

    # ✅ Build the Application correctly
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_button))

    logger.info("Bot is running...")

    # Run the bot asynchronously
    await app.run_polling()

try:
    loop = asyncio.get_running_loop()
    loop.stop()
except RuntimeError:
    pass  # No running loop exists

asyncio.run(main())



if __name__ == "__main__":
    import asyncio


    async def main():
        print("Bot is starting...")
        # Your bot logic here...


    if __name__ == "__main__":
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        except RuntimeError as e:
            print(f"Error: {e}")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
