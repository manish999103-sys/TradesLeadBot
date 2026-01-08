import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running ✅")
async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if len(context.args) != 1:
        await update.message.reply_text("❌ Use: /access CODE")
        return

    code = context.args[0]

    with open("codes.json", "r") as f:
        codes = json.load(f)

    if code not in codes:
        await update.message.reply_text("❌ Invalid code")
        return

    if codes[code] != "unused":
        await update.message.reply_text("❌ Code already used")
        return

    with open("users.json", "r") as f:
        users = json.load(f)

    users[user_id] = True
    codes[code] = user_id

    with open("users.json", "w") as f:
        json.dump(users, f)

    with open("codes.json", "w") as f:
        json.dump(codes, f)

    await update.message.reply_text("✅ Access granted 🔓")
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("access", access))
app.run_polling(drop_pending_updates=True)
