from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
import logging
import asyncio
import os
from dotenv import load_dotenv
from importlib.metadata import files

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Set up logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_media(chat, file_path, caption):
    """Send an audio or image file if it exists, otherwise log an error."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as media:
            if file_path.endswith(".ogg"):
                await chat.reply_audio(audio=media, caption=caption)
            elif file_path.endswith(".png"):
                await chat.reply_photo(photo=media, caption=caption)
    else:
        logger.error(f"File not found: {file_path}")
        await chat.reply_text(f"⚠️ File not found: {file_path}")


# Quiz Questions
quiz_questions = [
    {
        "question": "What is the time signature of a waltz?",
        "options": ["2/4", "3/4", "4/4", "6/8"],
        "correct": "3/4"
    },
    {
        "question": "Which note is a whole step above C?",
        "options": ["C#", "D", "E", "B"],
        "correct": "D"
    },
    {
        "question": "How many beats does a dotted half note get?",
        "options": ["2", "3", "4", "6"],
        "correct": "3"
    },
    {
        "question": "What would be the name of the following scale (D -> E -> F# -> G -> A -> B -> C# -> D)?",
        "options": ["D major", "E minor", "C major", "D minor"],
        "correct": "D major"
    },
    {
        "question": "What would be a trie tone major chord made from root note C?",
        "options": ["C -> E -> G", "C -> D# -> G", "C -> E -> G#", "C -> D# -> F#"],
        "correct": "C -> E -> G"
    },
    {
        "question": "according to the mood, guess the chord is major or minor?",
        "audio": "audio/minor_chord_q.ogg",
        "options": ["major", "minor"],
        "correct": "minor"
    }
]

# User points system
user_points = {}

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_points.setdefault(chat_id, 0)

    await update.message.reply_text(
        "Hello! Welcome to the Music Theory Bot.\n"
        "Choose a topic to start learning:",
        reply_markup=lesson_menu()
    )
    await update.message.reply_text("☕ Support us: Buy Me a Coffee - https://www.buymeacoffee.com/musicbot")

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Welcome and lesson menu\n"
        "/help - Show this help message\n"
        "/quiz - Take a music theory quiz\n"
        "\n☕ Support us: Buy Me a Coffee - https://www.buymeacoffee.com/musicbot"
    )

# Lesson Menu
def lesson_menu():
    keyboard = [
        [InlineKeyboardButton("Basics", callback_data="basics")],
        [InlineKeyboardButton("Rhythm", callback_data="rhythm")],
        [InlineKeyboardButton("Intervals", callback_data="intervals")],
        [InlineKeyboardButton("Scales", callback_data="scales")],
        [InlineKeyboardButton("Chords", callback_data="chords")],
        [InlineKeyboardButton("Quiz", callback_data="quiz")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Basics Lesson
async def basics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Send initial text
    await query.message.edit_text(
        "Basics of music theory:\n"
        "- Note lengths: 1 Whole note = 2 Half notes = 4 Quarter notes = 8 Eighth notes = 16 Sixteenth notes\n"
        "- Note names: C (Do), D (Re), E (Mi), F (Fa), G (Sol), A (La), B (Si).\n"
        "\nListen to the note lengths and pay attention to the image:"
    )

    # Define file paths
    files = [
        ("audio/note_durations.ogg", "Note lengths example."),
        ("image/note_lengths_image.png", "Visual representation of note lengths."),
        ("audio/notes.ogg", "Notes example."),
        ("image/notes_image.png", "Visual representation of notes."),
    ]

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text("Choose another lesson:", reply_markup=lesson_menu())

# Rhythm Lesson
async def rhythm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "Rhythm concepts:\n"
        "- Time signatures:\n"
        "  * Simple Rhythms: Each beat is divided into two equal parts (e.g., 2/4, 3/4, 4/4).\n"
        "  * Compound Rhythms: Each beat is divided into three equal parts (e.g., 6/8, 9/8, 12/8).\n"
        "- Tempo: Beats per minute (BPM).\n"
        "- Syncopation: Offbeat emphasis.\n"
        "\nChoose another lesson:"
    )

    files = [
        ("audio/Simple_rhythm_example.ogg", "Simple Rhythm Example"),
        ("audio/Compound_rhythm_example.ogg", "Compound Rhythm Example"),
    ]

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text("Choose another lesson:", reply_markup=lesson_menu())

# Interval Lesson
async def interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Properly formatted interval information
    text = (
        "- **Intervals**:\n"
        "Here are the basic intervals from smallest to an octave:\n\n"
        "🎵 **Minor Second (m2)** – 1 semitone (C → C# / Db)\n"
        "🎵 **Major Second (M2)** – 2 semitones (C → D)\n"
        "🎵 **Minor Third (m3)** – 3 semitones (C → Eb)\n"
        "🎵 **Major Third (M3)** – 4 semitones (C → E)\n"
        "🎵 **Perfect Fourth (P4)** – 5 semitones (C → F)\n"
        "🎵 **Tritone (A4/d5)** – 6 semitones (C → F# / Gb)\n"
        "🎵 **Perfect Fifth (P5)** – 7 semitones (C → G)\n"
        "🎵 **Minor Sixth (m6)** – 8 semitones (C → Ab)\n"
        "🎵 **Major Sixth (M6)** – 9 semitones (C → A)\n"
        "🎵 **Minor Seventh (m7)** – 10 semitones (C → Bb)\n"
        "🎵 **Major Seventh (M7)** – 11 semitones (C → B)\n"
        "🎵 **Perfect Octave (P8)** – 12 semitones (C → C)\n\n"
        "⬇️ Listen to the intervals below:"
    )

    files = [
        ("audio/Intervals.ogg", "Intervals Example"),
    ]

    await query.message.edit_text(text)

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text("Choose another lesson:", reply_markup=lesson_menu())

# Scales Lesson
async def scales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
     "major: C -> D -> E -> F -> G -> A -> B -> C \n "
     "minor : A -> B -> C -> D -> E -> F -> G -> A \n")

    files = [
        ("audio/scales.ogg", "scales"),
    ]

    await query.message.edit_text(text)

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text("Choose another lesson:", reply_markup=lesson_menu())

# Chords Lesson
async def chords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = ( "* Trie tone chords: \n"
     "major: C -> E (a major third farther, 2 whole steps or 4 half steps) -> G"
     "(a perfect fifth farther, 3/5 whole steps or 7 half steps (actually a minor third farther from the second note)) \n "
     "minor : C -> D# (a minor third farther, 1/5 whole steps or 3 half steps) -> G "
     "(a perfect fifth farther, 3/5 whole steps or 7 half steps (actually a major third farther from the second note)) \n"
     "after having listened to the examples go on and experience chords on your own instrument\n"
     "(ps: major chords have a happy filling in contrast to the minor chords)\n" )

    files = [
        ("audio/chords.ogg", "chords"),
    ]

    await query.message.edit_text(text)

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text("Choose another lesson:", reply_markup=lesson_menu())

# Send Quiz
async def send_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["quiz_index"] = 0  # Start at the first question
    await send_question(update, context)

# Send Question

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quiz_index = context.user_data.get("quiz_index", 0)
    chat_id = update.effective_chat.id

    if quiz_index >= len(quiz_questions):
        score = user_points.get(chat_id, 0)
        await update.effective_message.reply_text(
            f"🎉 Quiz complete! Your score: {score}/{len(quiz_questions)}\n"
            "Want to try again? Click below.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Restart Quiz", callback_data="quiz_restart")]])
        )
        return

    question_data = quiz_questions[quiz_index]
    keyboard = [[InlineKeyboardButton(option, callback_data=f"quiz_{option}")] for option in question_data["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 🎵 Send the audio file before the question (if it exists)
    if "audio" in question_data and question_data["audio"]:
        await send_media(update.effective_message, question_data["audio"], "Listen to this audio and answer:")

    # 📝 Send the question text after the audio
    await update.effective_message.reply_text(question_data["question"], reply_markup=reply_markup)

# Handle Button Clicks
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = update.effective_chat.id

    if data == "quiz":
        await send_quiz(update, context)
    elif data == "intervals":
        await interval(update, context)
    elif data == "basics":
        await basics(update, context)
    elif data == "rhythm":
        await rhythm(update, context)
    elif data == "chords":
        await chords(update, context)
    elif data == "scales":
        await scales(update, context)
    elif data == "quiz_restart":
        context.user_data["quiz_index"] = 0
        user_points[chat_id] = 0  # Reset points
        await send_quiz(update, context)
    elif data.startswith("quiz_"):
        selected_option = data.replace("quiz_", "")
        quiz_index = context.user_data.get("quiz_index", 0)

        if quiz_index < len(quiz_questions):
            correct_answer = quiz_questions[quiz_index]["correct"]
            if selected_option == correct_answer:
                user_points[chat_id] = user_points.get(chat_id, 0) + 1
                response = "✅ Correct! You earned 1 point."
            else:
                response = f"❌ Incorrect. The correct answer is {correct_answer}."

            await query.message.edit_text(text=response)
            context.user_data["quiz_index"] += 1
            await asyncio.sleep(2)
            await send_question(update, context)

# Main Function
def main():
    app = Application.builder().token(BOT_TOKEN).read_timeout(20).write_timeout(20).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quiz", send_quiz))
    app.add_handler(CallbackQueryHandler(handle_button))

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
