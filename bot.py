import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

# Your bot token
TOKEN = "9125574196:AAEU9gb07PEsCySt3oIORNT7LxULewCbvjQ"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

CHEAT_CODES = {
    "plr": {
        "title": "Pupillary Light Reflex (PLR)",
        "content": """
👁️ *Pupillary Light Reflex Cheat Code*

*Pathway (10-second version):*
1. Light → Optic Nerve (CN II) → Pretectal nucleus
2. Pretectal → *both* Edinger-Westphal nuclei
3. EW → Oculomotor (CN III) → Ciliary ganglion → Sphincter pupillae

*Key Clinical Points:*
• Direct + Consensual = intact pathway
• Afferent defect (RAPD) → CN II problem
• Efferent defect → CN III / sphincter problem
• Argyll Robertson pupil = pretectal lesion (reacts to accommodation, not light)
"""
    },
    "cranial": {
        "title": "Cranial Nerves",
        "content": """
🧠 *Cranial Nerves Order*
Oh Oh Oh To Touch And Feel Very Good Velvet Ah Heaven

I   Olfactory
II  Optic
III Oculomotor
IV  Trochlear
V   Trigeminal
VI  Abducens
VII Facial
VIII Vestibulocochlear
IX  Glossopharyngeal
X   Vagus
XI  Accessory
XII Hypoglossal

*Sensory / Motor / Both:*
Some Say Marry Money But My Brother Says Big Brains Matter More
"""
    },
    "abg": {
        "title": "ABG Interpretation",
        "content": """
🩸 *ABG Cheat Code (5 steps)*

1. Look at pH → Acidosis (<7.35) or Alkalosis (>7.45)
2. Look at PaCO₂ → Respiratory component
3. Look at HCO₃ → Metabolic component
4. Match the primary disturbance
5. Check compensation & anion gap if metabolic acidosis

*Remember:*
• Respiratory opposite (pH ↑ CO₂ ↓)
• Metabolic equal (pH ↑ HCO₃ ↑)
"""
    },
    "consort": {
        "title": "Study Design Guidelines",
        "content": """
📊 *CONSORT / STROBE / PRISMA*

• CONSORT → Randomized Controlled Trials (RCTs)
• STROBE → Observational studies
• PRISMA → Systematic reviews & meta-analyses

Mnemonic:
Clinical trials → CONSORT
Observational → STROBE
Systematic → PRISMA
"""
    },
    "heart": {
        "title": "Heart Sounds & Murmurs",
        "content": """
❤️ *Heart Sounds Cheat Code*

S1 = Mitral + Tricuspid closure (start of systole)
S2 = Aortic + Pulmonary closure (start of diastole)

*Common Murmurs:*
• AS → Ejection systolic, radiates to carotids
• MR → Pansystolic, radiates to axilla
• MS → Mid-diastolic, opening snap
• AR → Early diastolic
"""
    },
    "diabetes": {
        "title": "Diabetes Drugs (Quick)",
        "content": """
💉 *Diabetes Drugs Cheat Code*

• Metformin → First line (reduces hepatic glucose)
• SGLT2i (flozins) → Heart & kidney protection
• GLP-1 (tides) → Weight loss + heart benefit
• DPP-4 (gliptins) → Weight neutral
• Sulfonylureas → Hypoglycemia risk
• Insulin → When others fail or severe hyperglycemia
"""
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Cranial Nerves", callback_data="cranial")],
        [InlineKeyboardButton("👁️ Pupillary Light Reflex", callback_data="plr")],
        [InlineKeyboardButton("🩸 ABG Basics", callback_data="abg")],
        [InlineKeyboardButton("❤️ Heart Sounds", callback_data="heart")],
        [InlineKeyboardButton("💉 Diabetes Drugs", callback_data="diabetes")],
        [InlineKeyboardButton("📊 Study Designs", callback_data="consort")],
        [InlineKeyboardButton("📋 Show All Codes", callback_data="list")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👨‍⚕️ *Welcome to MedCheatCode Bot!*\n\n"
        "I give you high-yield medical mnemonics & cheat codes.\n\n"
        "⚠️ *For educational use only* – not medical advice.\n\n"
        "Choose a topic below or type a keyword (example: `plr`, `cranial`, `abg`):",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start – Open main menu\n"
        "/help – Show this help\n"
        "/list – Show all cheat codes\n\n"
        "You can also just type keywords like:\n"
        "`plr`, `cranial`, `abg`, `heart`, `diabetes`"
    )

async def list_codes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "*Available Cheat Codes:*\n\n"
    for key, data in CHEAT_CODES.items():
        text += f"• `{key}` → {data['title']}\n"
    text += "\nType any key above to get the full content."
    await update.message.reply_text(text, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "list":
        text = "*Available Cheat Codes:*\n\n"
        for key, value in CHEAT_CODES.items():
            text += f"• `{key}` → {value['title']}\n"
        text += "\nType any key to get the full cheat code."
        await query.edit_message_text(text, parse_mode="Markdown")
        return

    if data in CHEAT_CODES:
        code = CHEAT_CODES[data]
        await query.edit_message_text(
            f"*{code['title']}*\n{code['content']}",
            parse_mode="Markdown",
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in CHEAT_CODES:
        code = CHEAT_CODES[text]
        await update.message.reply_text(
            f"*{code['title']}*\n{code['content']}",
            parse_mode="Markdown",
        )
        return

    matches = []
    for key, data in CHEAT_CODES.items():
        if text in key or text in data["title"].lower():
            matches.append(f"• `{key}` → {data['title']}")

    if matches:
        await update.message.reply_text(
            "I found these:\n\n" + "\n".join(matches) + "\n\nType the key to see the full cheat code.",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            "No match found.\n\nTry typing one of these:\n"
            "`plr`  `cranial`  `abg`  `heart`  `diabetes`  `consort`\n\n"
            "Or use /list to see all."
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_codes))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("MedCheatCode Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_codes))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("MedCheatCode Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    