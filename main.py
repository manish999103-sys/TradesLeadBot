import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters
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

    users[user_id] = ""
    codes[code] = user_id

    with open("users.json", "w") as f:
        json.dump(users, f)

    with open("codes.json", "w") as f:
        json.dump(codes, f)

    await update.message.reply_text("✅ Access granted 🔓")
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("access", access))
app.add_handler(CommandHandler("setmsg", setmsg))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    with open("users.json", "r") as f:
        users = json.load(f)

    if user_id not in users:
        return

    message = users[user_id]

    if not message:
        return

    await update.message.reply_text(message)

async def setmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    with open("users.json", "r") as f:
        users = json.load(f)

    if user_id not in users:
        await update.message.reply_text("❌ Access denied. Buy access first.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("❌ Use: /setmsg Your auto message")
        return

    message = " ".join(context.args)

    users[user_id] = message   # ✅ YAHI MAIN LINE HAI

    with open("users.json", "w") as f:
        json.dump(users, f)

    await update.message.reply_text("✅ Auto message saved!")
app.run_polling(drop_pending_updates=True)
