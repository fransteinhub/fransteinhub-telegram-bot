from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

TOKEN = os.environ.get("8246231056:AAFyqwa7tSi5vLZx1C2GDr96PQwscKDSpms").

def start(update, context):
    update.message.reply_text(
        "Welcome to Franstein's Hub Engagement Community!\n\n"
        "Use /register to join."
    )

def register(update, context):
    user = update.effective_user
    update.message.reply_text(
        f"Registration successful!\nUsername: @{user.username}"
    )

def pay(update, context):
    update.message.reply_text(
        "Monthly Payment:\n"
        "Nigeria: ₦500\n"
        "Other countries: Equivalent\n\n"
        "Pay here:\n"
        "https://flutterwave.com/pay/4slkmziqetp9"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("pay", pay))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
