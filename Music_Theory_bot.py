import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import random

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Set up logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_text(language_code, key):
    """Retrieve the text in the specified language."""
    if language_code not in LANGUAGES:
        logger.warning(f"Missing language support for: {language_code}")
    return LANGUAGES.get(language_code, LANGUAGES["en"]).get(key, key)

lessons = {
    "en": {
        "basics": {
            "text": "Basics of music theory:\n"
                    "- Note lengths: 1 Whole note = 2 Half notes = 4 Quarter notes = 8 Eighth notes = 16 Sixteenth notes\n"
                    "- Note names: C (Do), D (Re), E (Mi), F (Fa), G (Sol), A (La), B (Si).\n"
                    "\nListen to the note lengths and pay attention to the image:",
            "files": [
                ("audio/note_durations.ogg", "note_lengths_example"),
                ("image/note_lengths_image.png", "note_lengths_image"),
                ("audio/notes.ogg", "notes_example"),
                ("image/notes_image.png", "notes_image"),
            ],
            "choose_lesson": "Choose another lesson:"
        },
        "rhythm": {
            "text": "Rhythm concepts:\n"
                    "- Time signatures:\n"
                    "  * Simple Rhythms: Each beat is divided into two equal parts (e.g., 2/4, 3/4, 4/4).\n"
                    "  * Compound Rhythms: Each beat is divided into three equal parts (e.g., 6/8, 9/8, 12/8).\n"
                    "- Tempo: Beats per minute (BPM).\n"
                    "- Syncopation: Offbeat emphasis.\n"
                    "\nChoose another lesson:",
            "files": [
                ("audio/Simple_rhythm_example.ogg", "simple_rhythm_example"),
                ("audio/Compound_rhythm_example.ogg", "compound_rhythm_example"),
            ],
            "choose_lesson": "Choose another lesson:"
            }},

    "es": {
        "basics": {
            "text": "Conceptos básicos de la teoría musical:\n"
                    "- Duraciones de notas: 1 redonda = 2 blancas = 4 negras = 8 corcheas = 16 semicorcheas\n"
                    "- Nombres de notas: C (Do), D (Re), E (Mi), F (Fa), G (Sol), A (La), B (Si).\n"
                    "\nEscucha las duraciones de las notas y observa la imagen:",
            "files": [
                ("audio/note_durations.ogg", "ejemplo_duraciones_notas"),
                ("image/note_lengths_image.png", "imagen_duraciones_notas"),
                ("audio/notes.ogg", "ejemplo_notas"),
                ("image/notes_image.png", "imagen_notas"),
            ],
            "choose_lesson": "Elige otra lección:"
        },
        "rhythm": {
            "text": "Conceptos de ritmo:\n"
                    "- Signaturas de tiempo:\n"
                    "  * Ritmos simples: Cada pulso se divide en dos partes iguales (ej., 2/4, 3/4, 4/4).\n"
                    "  * Ritmos compuestos: Cada pulso se divide en tres partes iguales (ej., 6/8, 9/8, 12/8).\n"
                    "- Tempo: PPM (Pulsos por minuto).\n"
                    "- Síncopa: Énfasis en el contratiempo.\n"
                    "\nElige otra lección:",
            "files": [
                ("audio/Simple_rhythm_example.ogg", "ejemplo_ritmo_simple"),
                ("audio/Compound_rhythm_example.ogg", "ejemplo_ritmo_compuesto"),
            ],
            "choose_lesson": "Elige otra lección:"
            }},

    "fr": {
        "basics": {
            "text": "Notions de base en théorie musicale:\n"
                    "- Durées des notes: 1 ronde = 2 blanches = 4 noires = 8 croches = 16 double-croches\n"
                    "- Noms des notes: C (Do), D (Ré), E (Mi), F (Fa), G (Sol), A (La), B (Si).\n"
                    "\nÉcoutez les durées des notes et regardez l’image:",
            "files": [
                ("audio/note_durations.ogg", "exemple_durees_notes"),
                ("image/note_lengths_image.png", "image_durees_notes"),
                ("audio/notes.ogg", "exemple_notes"),
                ("image/notes_image.png", "image_notes"),
            ],
            "choose_lesson": "Choisissez une autre leçon:"
        },
        "rhythm": {
            "text": "Concepts du rythme:\n"
                    "- Signatures temporelles:\n"
                    "  * Rythmes simples : Chaque battement est divisé en deux parties égales (ex. : 2/4, 3/4, 4/4).\n"
                    "  * Rythmes composés : Chaque battement est divisé en trois parties égales (ex. : 6/8, 9/8, 12/8).\n"
                    "- Tempo : Battements par minute (BPM).\n"
                    "- Syncopation : Accentuation hors temps.\n"
                    "\nChoisissez une autre leçon:",
            "files": [
                ("audio/Simple_rhythm_example.ogg", "exemple_rythme_simple"),
                ("audio/Compound_rhythm_example.ogg", "exemple_rythme_composé"),
            ],
            "choose_lesson": "Choisissez une autre leçon:"
    }}
}
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
        "options": ["2/4", "3/4", "4/4", "6/8"],
        "correct": "3/4"
    },
    {
        "question": "¿Qué nota está un paso por encima de C?",
        "options": ["C#", "D", "E", "B"],
        "correct": "D"
    },
    {
        "question": "¿Cuántos tiempos tiene una blanca con puntillo?",
        "options": ["2", "3", "4", "6"],
        "correct": "3"
    },
    {
        "question": "¿Cuál sería el nombre de la siguiente escala (D -> E -> F# -> G -> A -> B -> C# -> D)?",
        "options": ["Re mayor", "Mi menor", "Do mayor", "Re menor"],
        "correct": "Re mayor"
    },
    {
        "question": "¿Cuál sería un acorde mayor trie tono hecho a partir de la nota fundamental C?",
        "options": ["C -> Mi -> Sol", "C -> Re# -> Sol", "C -> Mi -> Sol#", "C -> Re# -> Fa#"],
        "correct": "C -> E -> G"
    },
    {
        "question": "según el estado de ánimo, ¿adivinas que el acorde es mayor o menor?",
        "audio": "audio/minor_chord_q.ogg",
        "options": ["mayor", "menor"],
        "correct": "menor"
    }]
    }

amazon_adz = {
    "guitar": [
        ("🎸 Buy a Beginner Guitar", "https://www.amazon.ca/DONNER-DST-80-Electric-Guitar-Beginner/dp/B0DGX3931N/ref=sr_1_15?dib=eyJ2IjoiMSJ9.BWv838_pZEJ8XWxZEqfLXM-40IFxC0aZgKxs4jMW8upGDu2r4LekmIyKVEqhHcH_yWYXqy5uvBhY3puObtnah-lIWpQ9ph1W8_YXhk9ni7RYhZmSQXUSVMifnB2ibGpKK_yR3_eDFZAB95hnJQYgx_mytvKmGZ7Dx720A6ohLZYvh4N4eQgrxyCEtbgU1MSfAp0G-HQL05dA1NTBQ8RfEtPz0TeJd4G2jKLUb5NwadZVQBjeY02vt4AqmyHJHcOo2GY292RJ4x5TK0UTchSBCh1Yms7SgoO67S0KWVgGYKA.z346u3gX8GIiM6djky_bseCQ6ZhECSv0oMK_qVHP_n4&dib_tag=se&keywords=Guitars%2Bfor%2BBeginners&qid=1744207296&sr=8-15&th=1"),
        ("🎶 Guitar Strings Pack", "https://www.amazon.ca/Ernie-Ball-Regular-Electric-Strings/dp/B09WZ8PVZH/ref=sr_1_4?crid=2OSVY4T6053EP&dib=eyJ2IjoiMSJ9.vMGZlxLRqkGt-OQDB8V2Pmbqzam3s92SA9uaE_BeKgYHXYalWc4SNeeNAJrqlSqPVMpSChRd9p4jC1TbMT4FsBeWeTS5tGemUy_tR76687DeBxE_ZJoIR_numJxFrn54u4DPrUBRiicBeaeXFutMrmKADyZw6c_TSPVxNYVZ2jecGqcFLf7giMtOb4gp_ZpCn84G1CMrzHQWzsaylAw26CtZCuktmp6p2m7HzoVLoBcTG3GvoPI9HYiEOeOelgy9O8L8KS7AMmWeu2oegPO7RrBvuZzo_wR0nmRymHTXHeU.FKXB9sDdtmL1OsLWULmfvWSrzHjZW6cY013vTbW5HNg&dib_tag=se&keywords=guitar%2Bstrings%2Bpack&qid=1744207590&s=musical-instruments&sprefix=guitar%2Bstrings%2Bpac%2Cmi%2C309&sr=1-4&th=1")
    ],
    "books": [
        ("📘 Music Theory For Dummies", "https://www.amazon.ca/Guitar-Fretboard-Memorize-Exercises-Included/dp/1719064873/ref=sr_1_2_sspa?dib=eyJ2IjoiMSJ9.wd9U0cX3cvv4KcRCIEkOQjJXBXDDI0eeOB_k5eCPWPBnSm4LisWnS78fzvHJSv1L4qmeYD-jNV6Y0cRExZlwRAAPtAEUA67q8Hex5LyG0AXmmddKrQKRTANXmy9-aVxjSJs0Hl3qLs6k0eh2C9B-Qhwrf_IAN0ltZabd6zpRHPRj4CmR_Hzv-VpcLNddD_ixzmK84aQogx78ChnFC6m6jBBTfCFhnWiZsPt_E63JOLSpI7kPNII03oEd_p9uabmvB-OLHkXQPAlTl-bAMDcJ8YXyfp2Qj4LE-gBYuTbpMU0.fXx5atBKU3wowglMSMcpWnptQHQYGj3uxX3fD-ycTHY&dib_tag=se&keywords=guitar+book&qid=1744207823&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"),
        ("guitar fret board", "https://www.amazon.ca/Guitar-Adult-Beginners-Step-Step/dp/B0DT89T5B3/ref=sr_1_5_sspa?crid=34FM4DRF3A5TW&dib=eyJ2IjoiMSJ9.OrciLYa5RlM59RUC7adPX51Ths9hHfMoNQVR8zwU2rskcg_iTqpzd-ngAb52XLOM_rYfbw8CjCawdr2jU73Y4SOfpm9l-JiAVV-9iew_iNC0mPqI0VWEL4ng3ZzhOHKV_ToWPZYAp2WMNHAPxz4tfPLy2oPp4s1zWNn300_atoEuYKJ0rbd9nRw63BfmqKVQvHH80qAIv71tDjEe-W9QKlskXoKw6WoFWVJobedXDPJyKVBBY9cZN06mJZM_G5MTZaES_OrhrqBxILo_ojg57WPXzlgFOZkVMDtJHpY1_n8.oQj_ktZaKk1wLQ9xGBiqvm33OQbAhWwSI9rzu9Y05VU&dib_tag=se&keywords=guitar+book+best+seller&qid=1744207985&sprefix=guitar+book+best+selle%2Caps%2C522&sr=8-5-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1")
    ]
}

async def send_media(chat, file_path, caption="", is_quiz=False):
    """Send OGG media files, handling quiz and lesson media separately."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        await chat.send_message("⚠️ Media file unavailable. Please try again later.")
        return

    with open(file_path, "rb") as media:
        if file_path.endswith(".ogg"):
            if is_quiz:
                await chat.send_audio(audio=media, caption=caption or "🎵 Quiz Audio: Listen and answer.")
            else:
                await chat.reply_voice(voice=media, caption=caption or "🔊 Lesson Audio:")
        elif file_path.endswith(".png"):  # Image handling
            await chat.reply_photo(photo=media, caption=caption or "🖼️ Lesson Image:")
        #else:
            #await chat.send_message("⚠️ Unsupported file format. Only .ogg files are allowed.")

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   # logger.info(f"Received /start command from {update.effective_user.id}")
    #try:
     #   await update.message.reply_text("Hello, this is a test response!")
      #  logger.info("Successfully sent response.")
    #except Exception as e:
     #   logger.error(f"Error sending message: {e}")
    chat_id = update.effective_chat.id
    #user_points.setdefault(chat_id, 0)
    if chat_id not in user_points:
        user_points[chat_id] = 0  # Ensure user has a score
    user_lang = update.effective_user.language_code[:2]  # Get the first two letters of the language code
    message = get_text(user_lang, "start")

    # Inline button for support
    support_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("☕ Buy Me a Coffee", url="https://www.buymeacoffee.com/musicbot")]]
    )

    await update.message.reply_text(
        message,
        reply_markup=lesson_menu(user_lang),
    )

    await update.message.reply_text(
        "Support us:", reply_markup=support_keyboard
    )

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

#  Amazon ad sender
def get_anazon_ad_keybord (category: "books"):
    buttons = []
    if category in amazon_adz:
        ads = random.sample(amazon_adz[category], k=min(2, len(amazon_adz[category])))
        for text, url in ads:
            buttons.append([InlineKeyboardButton(text, url=url)])
    return InlineKeyboardMarkup(buttons)

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
    chat_id = update.effective_chat.id
    quiz_data = context.user_data.get("quiz", {})
    questions = quiz_data.get("questions", [])
    current_index = quiz_data.get("current_index", 0)

    if current_index >= len(questions):
        score = user_points.get(chat_id, 0)
        user_lang = update.effective_user.language_code[:2]

        # Create a combined reply markup with both "Restart Quiz" and "Lesson Menu"
        keyboard = [
            [InlineKeyboardButton("🔄 Restart Quiz", callback_data="quiz_restart")],
            [InlineKeyboardButton("📚 Lesson Menu", callback_data="lesson_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.effective_message.reply_text(
            f"🎉 Quiz complete! Your score: {score}/{len(questions)}\n"
            "Want to try again? Click below.\n"
            "If not, choose another lesson:",
            reply_markup=reply_markup
        )
        return

    # Store the current question in user_data
    question_data = questions[current_index]
    context.user_data["current_question"] = question_data  # 🔴 This is the missing line!

    # Send the question
    question_text = question_data["question"]
    options = question_data["options"]

    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{i}")] for i, opt in enumerate(options)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_message.reply_text(question_text, reply_markup=reply_markup)

    # If the question has an audio file, send it
    if "audio" in question_data:
        audio_path = question_data["audio"]
        await send_media(update.effective_chat, audio_path, is_quiz=True)

    # Sending the ads
    await update.message.reply_text(
        "Recommended for you:",
        reply_markup = get_anazon_ad_keybord("guitar")
    )

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
    elif data == "quiz":
        await send_quiz(update, context)
    elif data == "lesson_menu":
        user_lang = update.effective_user.language_code[:2]
        await query.message.reply_text("📚 Choose a lesson:", reply_markup=lesson_menu(user_lang))
    elif data.startswith("quiz_"):
        await query.answer()  # Ensure the query is answered
        print(f"Received callback data: {data}")  # Debugging

        callback_data = query.data  # Example: "quiz_1"
        selected_option = data.replace("quiz_", "")

        quiz_data = context.user_data.get("quiz", {})

        questions = quiz_data.get("questions", [])
        current_index = quiz_data.get("current_index", 0)

        # ✅ Handle quiz restart separately
        if selected_option == "restart":
            await send_quiz(update, context)  # Function to restart the quiz
            return

        # Check if the selected option is actually a number
        if not selected_option.isdigit():
            print(f"Error: Invalid quiz callback data received: {selected_option}")  # Debugging
            await query.answer("Invalid selection. Please try again.")
            return

        option_index = int(callback_data.replace("quiz_", ""))  # Converts "quiz_1" to 1
        print(f"Option index: {option_index}")  # Debugging

        question_data = context.user_data.get("current_question", {})

        options = question_data.get("options", [])

        if option_index < 0 or option_index >= len(options):
            print("Invalid selection detected!")  # Debugging
            await query.answer("Invalid selection. Please try again.")
            return

        answer_text = options[option_index]  # Retrieve the actual answer text

        if current_index < len(questions):
            answer_text = options[option_index].strip().lower()  # Convert to lowercase
            correct_answer = questions[current_index]["correct"].strip().lower()  # Convert to lowercase

            print(f"Selected answer: {answer_text}, Correct answer: {correct_answer}")

            if answer_text == correct_answer:
                user_points[chat_id] += 1
                await query.message.reply_text(get_text(user_lang, "quiz_correct"))
            else:
                await query.message.reply_text(f"{get_text(user_lang, 'quiz_wrong')} {correct_answer}")

            quiz_data["current_index"] += 1
            context.user_data["quiz"] = quiz_data

            await send_question(update, context)  # Move to next question

async def basics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_lang = update.effective_user.language_code[:2]  # Get user language (e.g., "en", "es", "fr")

    # Get lesson data, fallback to English if unavailable
    lesson_data = lessons.get(user_lang, lessons["en"]).get("basics", {})

    # Send lesson text
    await query.message.edit_text(lesson_data.get("text", "Lesson not available."))

    # Send media files with their corresponding translations
    for file_path, caption_key in lesson_data.get("files", []):
        await send_media(query.message, file_path, get_text(user_lang, caption_key))
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text(
        lesson_data.get("choose_lesson", "Choose another lesson:"),
        reply_markup=lesson_menu(user_lang)
    )

# Rhythm Lesson
async def rhythm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_lang = update.effective_user.language_code[:2]  # Get the user's language

    # Retrieve lesson data, fallback to English if unavailable
    lesson_data = lessons.get(user_lang, lessons["en"]).get("rhythm", {})

    # Send lesson text
    await query.message.edit_text(lesson_data.get("text", "Lesson not available."))

    # Send media files with localized captions
    for file_path, caption_key in lesson_data.get("files", []):
        await send_media(query.message, file_path, get_text(user_lang, caption_key))
        await asyncio.sleep(1)  # Pause between messages

    # Show lesson menu again
    await query.message.reply_text(
        lesson_data.get("choose_lesson", "Choose another lesson:"),
        reply_markup=lesson_menu(user_lang)
    )
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


# **Main function to start the bot**
def main():
    app = Application.builder().token(BOT_TOKEN).read_timeout(20).write_timeout(20).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quiz", send_quiz))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))
    app.add_handler(CallbackQueryHandler(handle_button, pattern=r"^quiz_\d+$"))

    webhook_url = f"{WEBHOOK_URL}/webhook"
    # Set webhook using bot's method (blocking or not, your choice)
    app.bot.set_webhook(url=webhook_url)

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        url_path="webhook",
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    main()
#https://www.amazon.ca/Otamatone-Touch-Sensitive-Electronic-Musical-Instrument/dp/B00MRJ8GXK/ref=sr_1_22?crid=27SDGO4UILMCD&dib=eyJ2IjoiMSJ9.FtV5dPOYidmFp9wbNNNjqG3jk0ohn8UEzFxoxtgISo9WpN2MXnO8ZAJnw7TzLeJLrE7uvgYyDeY9AnUVrP7yUEw7JIFJwIneeMvJiRjWjCA2R7YUlzlHv4vuL08hKpz480C0GPaXhPFu5AGB2c2bZFMqxxwjOkRKu93Uu5rc5VrezuWIhlalI-HmxY0k0PddsBfrAGQI-v6VokAH1fMLjThJleVs37jBoK2ztnpqWb4RUasMfqk6sxP1_da2VfPSLQn9vm-k7ngkMJ6wcLarzYseUp11uOU3WVZo_VhQZV8.oxoEKI4ng2C0-bN8i5yz5HEo9A9ftZI36tTXG2Vy_qI&dib_tag=se&keywords=music&qid=1744116393&sprefix=mus%2Caps%2C333&sr=8-22&th=1
#https://www.amazon.ca/Donner-DMS-1-Portable-Tabletop-Ukulele/dp/B0772MTRSH/ref=pd_rhf_se_s_pd_sbs_rvi_d_sccl_2_5/133-1693958-3926168?pd_rd_w=7oPN5&content-id=amzn1.sym.7640e302-a2f4-4636-8c01-032f9fc35b54&pf_rd_p=7640e302-a2f4-4636-8c01-032f9fc35b54&pf_rd_r=Y1EXZSV606WWW920H549&pd_rd_wg=8RhMK&pd_rd_r=559fc661-261e-4ea9-955c-e813c1f330a5&pd_rd_i=B0772MTRSH&th=1
#https://www.amazon.ca/MOREYES-Composition-Manuscript-Notebook-notebook/dp/B07QCXR1SM/ref=sr_1_17?crid=27SDGO4UILMCD&dib=eyJ2IjoiMSJ9.FtV5dPOYidmFp9wbNNNjqG3jk0ohn8UEzFxoxtgISo9WpN2MXnO8ZAJnw7TzLeJLrE7uvgYyDeY9AnUVrP7yUEw7JIFJwIneeMvJiRjWjCA2R7YUlzlHv4vuL08hKpz480C0GPaXhPFu5AGB2c2bZFMqxxwjOkRKu93Uu5rc5VrezuWIhlalI-HmxY0k0PddsBfrAGQI-v6VokAH1fMLjThJleVs37jBoK2ztnpqWb4RUasMfqk6sxP1_da2VfPSLQn9vm-k7ngkMJ6wcLarzYseUp11uOU3WVZo_VhQZV8.oxoEKI4ng2C0-bN8i5yz5HEo9A9ftZI36tTXG2Vy_qI&dib_tag=se&keywords=music&qid=1744116393&sprefix=mus%2Caps%2C333&sr=8-17
#https://www.amazon.ca/GLEAM-Sheet-Music-Stand-Carrying/dp/B07D7QN1Z1/ref=sr_1_24?crid=27SDGO4UILMCD&dib=eyJ2IjoiMSJ9.FtV5dPOYidmFp9wbNNNjqG3jk0ohn8UEzFxoxtgISo9WpN2MXnO8ZAJnw7TzLeJLrE7uvgYyDeY9AnUVrP7yUEw7JIFJwIneeMvJiRjWjCA2R7YUlzlHv4vuL08hKpz480C0GPaXhPFu5AGB2c2bZFMqxxwjOkRKu93Uu5rc5VrezuWIhlalI-HmxY0k0PddsBfrAGQI-v6VokAH1fMLjThJleVs37jBoK2ztnpqWb4RUasMfqk6sxP1_da2VfPSLQn9vm-k7ngkMJ6wcLarzYseUp11uOU3WVZo_VhQZV8.oxoEKI4ng2C0-bN8i5yz5HEo9A9ftZI36tTXG2Vy_qI&dib_tag=se&keywords=music&qid=1744116393&sprefix=mus%2Caps%2C333&sr=8-24
#musictheorybo-20