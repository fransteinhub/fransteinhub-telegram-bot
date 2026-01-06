import os
import sqlite3
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("8246231056:AAFyqwa7tSi5vLZx1C2GDr96PQwscKDSpms")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    full_name TEXT,
    username TEXT,
    reg_number TEXT,
    platforms TEXT,
    payment_status TEXT
)
""")
conn.commit()

# ---------------- HELPERS ----------------
def generate_reg():
    return f"FH-{random.randint(1000, 9999)}"

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Welcome to FransteinHub Engagement Community*\n\n"
        "📌 Before joining any engagement group, you MUST:\n"
        "1️⃣ Follow & subscribe to our official pages\n"
        "2️⃣ Select social media platforms\n"
        "3️⃣ Make monthly payment\n\n"
        "👉 Click *Continue* to proceed"
    )

    keyboard = [[InlineKeyboardButton("Continue ▶️", callback_data="continue")]]
    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---------------- CONTINUE ----------------
async def continue_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🔔 *Follow & Subscribe to ALL links below:*\n\n"
        "YouTube:\nhttps://www.youtube.com/@FransteinMedTV\n\n"
        "Facebook:\nhttps://www.facebook.com/profile.php?id=61584095433733\n\n"
        "Instagram:\nhttps://www.instagram.com/fransteinmedtv\n\n"
        "TikTok:\nhttps://tiktok.com/@fransteinmed_tv\n\n"
        "Twitter:\nhttps://x.com/FransteinMedTV\n\n"
      
      "✅ Once done, click *I Have Followed*"
    )

    keyboard = [[InlineKeyboardButton("I Have Followed ✅", callback_data="followed")]]
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---------------- PLATFORM SELECTION ----------------
async def followed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("YouTube", callback_data="YT"),
         InlineKeyboardButton("Instagram", callback_data="IG")],
        [InlineKeyboardButton("TikTok", callback_data="TT"),
         InlineKeyboardButton("Facebook", callback_data="FB")],
        [InlineKeyboardButton("Twitter", callback_data="TW"),
         
        [InlineKeyboardButton("Confirm Selection ✅", callback_data="confirm")]
    ]

    context.user_data["platforms"] = []

    await query.edit_message_text(
        "📊 *Select Social Media Platforms*\n"
        "You can choose ONE, MANY or ALL.\n\n"
        "Click platforms to select, then confirm.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---------------- HANDLE PLATFORM CLICK ----------------
async def platform_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    code = query.data

    if code not in context.user_data["platforms"]:
        context.user_data["platforms"].append(code)

    await query.answer(f"Selected: {', '.join(context.user_data['platforms'])}")

# ---------------- CONFIRM ----------------
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    platforms = ", ".join(context.user_data["platforms"])

    text = (
        "💳 *Monthly Payment Required*\n\n"
        "🇳🇬 Nigeria: ₦500\n"
        "🌍 Other countries: Equivalent\n\n"
        "🔗 Pay here:\n"
        "https://flutterwave.com/pay/4slkmziqetp9\n\n"
        f"📌 Selected Platforms:\n{platforms}\n\n"
        "After payment, use /register"
    )

    await query.edit_message_text(text, parse_mode="Markdown")

# ---------------- REGISTER ----------------
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    reg = generate_reg()
    platforms = ", ".join(context.user_data.get("platforms", []))

    cur.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?)",
        (
            user.id,
            user.full_name,
            user.username,
            reg,
            platforms,
            "PENDING"
        )
    )
    conn.commit()

    await update.message.reply_text(
        f"✅ *Registration Successful*\n\n"
        f"🆔 Reg Number: `{reg}`\n"
        f"📊 Platforms: {platforms}\n\n"
        "⏳ Payment verification pending.\n"
        "You will be added to groups after verification.",
        parse_mode="Markdown"
    )

# ---------------- AI FAQ (RULE-BASED) ----------------
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *FransteinHub FAQ*\n\n"
        "• Engagement boosts reach & monetization\n"
        "• Help others → others help you\n"
        "• Defaulters are removed automatically\n"
        "• Monthly payment is compulsory\n\n"
        "Ask admin if you need more help."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("faq", faq))

    app.add_handler(CallbackQueryHandler(continue_step, pattern="continue"))
    app.add_handler(CallbackQueryHandler(followed, pattern="followed"))
    app.add_handler(CallbackQueryHandler(platform_click, pattern="^(YT|IG|TT|FB|TW|SC)$"))
    app.add_handler(CallbackQueryHandler(confirm, pattern="confirm"))

    app.run_polling()

if __name__ == "__main__":
    main()
