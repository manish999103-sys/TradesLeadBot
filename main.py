import os
import json
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ---------------- LOAD FILES ----------------

if os.path.exists("codes.json"):
    with open("codes.json", "r") as f:
        codes = json.load(f)
else:
    codes = []

if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

# ---------------- COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome!\n\n"
        "Use /access <code> to activate\n"
        "Then use /setmsg <message>"
    )

async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /access YOUR_CODE")
        return

    code = context.args[0]
    user_id = str(update.effective_user.id)

    if code not in codes:
        await update.message.reply_text("❌ Invalid access code")
        return

    users[user_id] = ""
    codes.remove(code)

    with open("users.json", "w") as f:
        json.dump(users, f)

    with open("codes.json", "w") as f:
        json.dump(codes, f)

    await update.message.reply_text("✅ Access granted! Now use /setmsg")

async def setmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in users:
        await update.message.reply_text("❌ Buy access first")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /setmsg your message")
        return

    message = " ".join(context.args)
    users[user_id] = message

    with open("users.json", "w") as f:
        json.dump(users, f)

    await update.message.reply_text("✅ Auto message saved")

# ---------------- AUTO REPLY ----------------

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id in users and users[user_id]:
        await update.message.reply_text(users[user_id])

# ---------------- APP START ----------------

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("access", access))
app.add_handler(CommandHandler("setmsg", setmsg))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

app.run_polling()
