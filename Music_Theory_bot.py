import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
)

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
        await chat.reply_text("⚠️ Media file unavailable. Please try again later.")

def get_text(language_code, key):
    """Retrieve the text in the specified language."""
    if language_code not in LANGUAGES:
        logger.warning(f"Missing language support for: {language_code}")
    return LANGUAGES.get(language_code, LANGUAGES["en"]).get(key, key)


LANGUAGES = {
    "en": {
        "start": "Hello! Welcome to the Music Theory Bot. Choose a topic to start learning:",
        "help": "Available commands:\n/start - Welcome and lesson menu\n/help - Show this help message\n/quiz - Take a music theory quiz",
        "help_commands": "/start - Welcome and lesson menu\n/help - Show this help message\n/quiz - Take a music theory quiz",
        "quiz_question": "Here is your question:",
        "quiz_correct": "✅ Correct! You earned 1 point.",
        "quiz_wrong": "❌ Incorrect. The correct answer is",
        "quiz_done": "🎉 Quiz complete! Your score: {score}/{total}",
        "support": "☕ Support us: Buy Me a Coffee - https://www.buymeacoffee.com/musicbot",
        "basics": "Basics",
        "rhythm": "Rhythm",
        "intervals": "Intervals",
        "scales": "Scales",
        "chords": "Chords",
        "quiz": "Quiz",
        "basics_text": "Basics of music theory:\n- Note lengths...",
        "note_lengths_example": "Note lengths example.",
        "note_lengths_image": "Visual representation of note lengths.",
        "notes_example": "Notes example.",
        "notes_image": "Visual representation of notes.",
        "choose_another_lesson": "Choose another lesson:"
    },
    "fr": {
        "start": "Bonjour! Bienvenue sur le bot de théorie musicale. Choisissez un sujet pour commencer l'apprentissage :",
        "help": "Commandes disponibles:\n/start - Accueil et menu des leçons\n/help - Afficher ce message d'aide\n/quiz - Faire un quiz de théorie musicale",
        "help_commands": "/start - Accueil et menu des leçons\n/help - Afficher ce message d'aide\n/quiz - Faire un quiz de théorie musicale",
        "quiz_question": "Voici votre question :",
        "quiz_correct": "✅ Correct! Vous avez gagné 1 point.",
        "quiz_wrong": "❌ Incorrect. La bonne réponse est",
        "quiz_done": "🎉 Quiz terminé! Votre score: {score}/{total}",
        "support": "☕ Soutenez-nous: Achetez-moi un café - https://www.buymeacoffee.com/musicbot",
        "basics": "Bases",
        "rhythm": "Rythme",
        "intervals": "Intervalles",
        "scales": "Gammes",
        "chords": "Accords",
        "quiz": "Quiz",
        "basics_text": "Les bases de la théorie musicale:\n- Durées des notes...",
        "note_lengths_example": "Exemple de durées des notes.",
        "note_lengths_image": "Représentation visuelle des durées des notes.",
        "notes_example": "Exemple de notes.",
        "notes_image": "Représentation visuelle des notes.",
        "choose_another_lesson": "Choisir une autre leçon:"
    },
    "es": {
        "start": "¡Hola! Bienvenido al bot de teoría musical. Elige un tema para comenzar a aprender:",
        "help": "Comandos disponibles:\n/start - Bienvenida y menú de lecciones\n/help - Mostrar este mensaje de ayuda\n/quiz - Realizar una prueba de teoría musical",
        "help_commands": "/start - Bienvenida y menú de lecciones\n/help - Mostrar este mensaje de ayuda\n/quiz - Realizar una prueba de teoría musical",
        "quiz_question": "Aquí está tu pregunta:",
        "quiz_correct": "✅ ¡Correcto! Has ganado 1 punto.",
        "quiz_wrong": "❌ Incorrecto. La respuesta correcta es",
        "quiz_done": "🎉 ¡Prueba completada! Tu puntuación: {score}/{total}",
        "support": "☕ Apóyanos: Cómprame un café - https://www.buymeacoffee.com/musicbot",
        "basics": "Conceptos básicos",
        "rhythm": "Ritmo",
        "intervals": "Intervalos",
        "scales": "Escalas",
        "chords": "Acordes",
        "quiz": "Cuestionario",
        "basics_text": "Conceptos básicos de la teoría musical:\n- Duración de las notas...",
        "note_lengths_example": "Ejemplo de duración de notas.",
        "note_lengths_image": "Representación visual de la duración de las notas.",
        "notes_example": "Ejemplo de notas.",
        "notes_image": "Representación visual de las notas.",
        "choose_another_lesson": "Elige otra lección:"
    }
}

# Quiz Questions
quiz_questions ={
    "en":[
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
    ],
    "fr":[
    {
        "question": "Quelle est la signature rythmique d'une valse ?",
        "options": ["2/4", "3/4", "4/4", "6/8"],
        "correct": "3/4"
    },
    {
        "question": "Quelle note est un cran au dessus de C ?",
        "options": ["C#", "D", "E", "B"],
        "correct": "D"
    },
    {
        "question": "Combien de battements obtient une blanche pointée ?",
        "options": ["2", "3", "4", "6"],
        "correct": "3"
    },
    {
        "question": "Quel serait le nom de la gamme suivante (D -> E -> F# -> G -> A -> B -> C# -> D) ?",
        "options": ["Ré majeur", "Mi mineur", "Do majeur", "Ré mineur"],
        "correct": "ré majeur"
    },
    {
        "question": "Que serait un accord majeur à trois tons composé de la note fondamentale C ?",
        "options": ["C -> E -> G", "C -> D# -> G", "C -> E -> G#", "C -> D# -> F#"],
        "correct": "C -> E -> G"
    },
    {
        "question": "selon l'ambiance, devinez que l'accord est majeur ou mineur ?",
        "audio": "audio/minor_chord_q.ogg",
        "options": ["majeur", "mineur"],
        "correct": "mineur"
    }
    ],
    "es":[{
        "question": "¿Cuál es el compás de un vals?",
        "opciones": ["2/4", "3/4", "4/4", "6/8"],
        "correcto": "3/4"
    },
    {
        "question": "¿Qué nota está un paso por encima de C?",
        "opciones": ["C#", "D", "E", "B"],
        "correcto": "D"
    },
    {
        "question": "¿Cuántos tiempos tiene una blanca con puntillo?",
        "opciones": ["2", "3", "4", "6"],
        "correcto": "3"
    },
    {
        "question": "¿Cuál sería el nombre de la siguiente escala (D -> E -> F# -> G -> A -> B -> C# -> D)?",
        "opciones": ["Re mayor", "Mi menor", "Do mayor", "Re menor"],
        "correcto": "Re mayor"
    },
    {
        "question": "¿Cuál sería un acorde mayor trie tono hecho a partir de la nota fundamental C?",
        "opciones": ["C -> Mi -> Sol", "C -> Re# -> Sol", "C -> Mi -> Sol#", "C -> Re# -> Fa#"],
        "correcto": "C -> E -> G"
    },
    {
        "pregunta": "según el estado de ánimo, ¿adivinas que el acorde es mayor o menor?",
        "audio": "audio/minor_chord_q.ogg",
        "opciones": ["mayor", "menor"],
        "correcto": "menor"
    }]
    }

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_points.setdefault(chat_id, 0)
    user_lang = update.effective_user.language_code[:2]  # Get the first two letters of the language code
    message = get_text(user_lang, "start")
    support_message = get_text(user_lang, "support")

    await update.message.reply_text(get_text(user_lang, "start"),
        reply_markup=lesson_menu(user_lang)
    )
    await update.message.reply_text("☕ Support us: Buy Me a Coffee -")

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = update.effective_user.language_code[:2]  # Get the first two letters of the language code
    help_text = get_text(user_lang, "help")
    support_text = get_text(user_lang, "support")

    # Send localized help message
    await update.message.reply_text(help_text)

    # Send localized commands list
    await update.message.reply_text(
        get_text(user_lang, "help_commands")
    )

# Lesson Menu
def lesson_menu(user_lang):
    keyboard = [
        [InlineKeyboardButton(get_text(user_lang, "basics"), callback_data="basics")],
        [InlineKeyboardButton(get_text(user_lang, "rhythm"), callback_data="rhythm")],
        [InlineKeyboardButton(get_text(user_lang, "intervals"), callback_data="intervals")],
        [InlineKeyboardButton(get_text(user_lang, "scales"), callback_data="scales")],
        [InlineKeyboardButton(get_text(user_lang, "chords"), callback_data="chords")],
        [InlineKeyboardButton(get_text(user_lang, "quiz"), callback_data="quiz")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Send Quiz
async def send_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = update.effective_user.language_code[:2]  # Get the first two letters of the language code

    # Default to English if the user's language is not available
    if user_lang not in quiz_questions:
        user_lang = "en"

    # Get the quiz questions for the user's language
    context.user_data["quiz"] = {
        "questions": quiz_questions[user_lang],
        "current_index": 0,
        "score": 0
    }

    # Call send_question to show the first question
    await send_question(update, context)

# User points system
user_points = {}

# Send Question
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the current question index and quiz data
    quiz_data = context.user_data.get("quiz", {})
    questions = quiz_data.get("questions", [])
    current_index = quiz_data.get("current_index", 0)

    if current_index >= len(questions):
        score = user_points.get("score", 0)
        await update.effective_message.reply_text(
            f"🎉 Quiz complete! Your score: {score}/{len(quiz_questions)}\n"
            "Want to try again? Click below.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Restart Quiz", callback_data="quiz_restart")]])
        )
        return

    # Get the current question
    question_data = questions[current_index]

    # Send the question and options
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in question_data["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_message.reply_text(question_data["question"], reply_markup=reply_markup)
    # Send text or audio question
    if "audio" in question_data:
        await update.message.reply_voice(voice=open(question_data["audio"], "rb"))
        await update.message.reply_text(question_data["question"])

# Handle Button Clicks
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE, user_lang="en"):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = update.effective_chat.id

    if data == "intervals":
        await interval(update, context)
    elif data == "basics":
        await basics(update, context)
    elif data == "rhythm":
        await rhythm(update, context)
    elif data == "chords":
        await chords(update, context)
    elif data == "scales":
        await scales(update, context)
        # Quiz logic
    elif data == "quiz":
            await send_quiz(update, context)
    elif data.startswith("quiz_"):
            selected_option = data.replace("quiz_", "")
            quiz_data = context.user_data.get("quiz", {})
            questions = quiz_data.get("questions", [])
            current_index = quiz_data.get("current_index", 0)

            if current_index < len(questions):
                correct_answer = questions[current_index]["correct"]
                if selected_option == correct_answer:
                    user_points[chat_id] += 1
                    await query.message.reply_text(get_text(user_lang, "quiz_correct"))
                else:
                    await query.message.reply_text(f"{get_text(user_lang, 'quiz_wrong')} {correct_answer}")

                # Move to next question
                quiz_data["current_index"] += 1
                context.user_data["quiz"] = quiz_data

                await send_question(update, context)


async def basics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_lang = update.effective_user.language_code[:2]  # Get the language of the user
    await query.message.edit_text(
        get_text(user_lang, "Basics of music theory:\n"
        "- Note lengths: 1 Whole note = 2 Half notes = 4 Quarter notes = 8 Eighth notes = 16 Sixteenth notes\n"
        "- Note names: C (Do), D (Re), E (Mi), F (Fa), G (Sol), A (La), B (Si).\n"
        "\nListen to the note lengths and pay attention to the image:")  # Use get_text() for the lesson content
    )

    files = [
        ("audio/note_durations.ogg", get_text(user_lang, "note_lengths_example")),
        ("image/note_lengths_image.png", get_text(user_lang, "note_lengths_image")),
        ("audio/notes.ogg", get_text(user_lang, "notes_example")),
        ("image/notes_image.png", get_text(user_lang, "notes_image")),
    ]

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text(get_text(user_lang, "choose_another_lesson"), reply_markup=lesson_menu(user_lang))

# Rhythm Lesson
async def rhythm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_lang = update.effective_user.language_code[:2]  # Get the language of the user
    await query.message.edit_text(
        get_text(user_lang,"Rhythm concepts:\n"
        "- Time signatures:\n"
        "  * Simple Rhythms: Each beat is divided into two equal parts (e.g., 2/4, 3/4, 4/4).\n"
        "  * Compound Rhythms: Each beat is divided into three equal parts (e.g., 6/8, 9/8, 12/8).\n"
        "- Tempo: Beats per minute (BPM).\n"
        "- Syncopation: Offbeat emphasis.\n"
        "\nChoose another lesson:")  # Use get_text() for the lesson content
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
    await query.message.reply_text(get_text(user_lang, "choose_another_lesson"), reply_markup=lesson_menu(user_lang))

# Interval Lesson
async def interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_lang = update.effective_user.language_code[:2]  # Get the language of the user
    await query.message.edit_text(
        get_text(user_lang,"- **Intervals**:\n"
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
        "⬇️ Listen to the intervals below:")  # Use get_text() for the lesson content
    )

    files = [
        ("audio/Intervals.ogg", "Intervals Example"),
    ]

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text(get_text(user_lang, "choose_another_lesson"), reply_markup=lesson_menu(user_lang))

# Scales Lesson
async def scales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_lang = update.effective_user.language_code[:2]  # Get the language of the user
    await query.message.edit_text(
        get_text(user_lang,"major: C -> D -> E -> F -> G -> A -> B -> C \n "
     "minor : A -> B -> C -> D -> E -> F -> G -> A \n")  # Use get_text() for the lesson content
    )

    files = [
        ("audio/scales.ogg", "scales"),
    ]

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text(get_text(user_lang, "choose_another_lesson"), reply_markup=lesson_menu(user_lang))

# Chords Lesson
async def chords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_lang = update.effective_user.language_code[:2]  # Get the language of the user
    await query.message.edit_text(
        get_text(user_lang, "* Trie tone chords: \n"
     "major: C -> E (a major third farther, 2 whole steps or 4 half steps) -> G"
     "(a perfect fifth farther, 3/5 whole steps or 7 half steps (actually a minor third farther from the second note)) \n "
     "minor : C -> D# (a minor third farther, 1/5 whole steps or 3 half steps) -> G "
     "(a perfect fifth farther, 3/5 whole steps or 7 half steps (actually a major third farther from the second note)) \n"
     "after having listened to the examples go on and experience chords on your own instrument (: \n"
     "(ps: major chords have a happy mood in contrast to the minor chords)\n")  # Use get_text() for the lesson content
    )

    files = [
        ("audio/chords.ogg", "chords"),
    ]

    # Check if the audio file exists before sending
    for file_path, caption in files:
        await send_media(query.message, file_path, caption)
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text(get_text(user_lang, "choose_another_lesson"), reply_markup=lesson_menu(user_lang))


# Main Function
def main():
    app = Application.builder().token(BOT_TOKEN).read_timeout(20).write_timeout(20).build()

    app.run_webhook(listen="0.0.0.0", port=8443, url_path="YOUR_BOT_TOKEN")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quiz", send_quiz))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))  # Handle answers

    #WEBHOOK_URL = "https://yourserver.com/webhook"
    #async def set_webhook():
       #await app.bot.set_webhook(WEBHOOK_URL)

    #asyncio.run(set_webhook())  # Set webhook on startup

    #app.run_webhook(listen="0.0.0.0", port=8443, webhook_url=WEBHOOK_URL)

    logger.info("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
