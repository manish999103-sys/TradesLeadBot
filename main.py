import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# -------- LOAD FILES --------

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

# -------- COMMANDS --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome 🤖\n\n"
        "/access CODE\n"
        "/setmsg MESSAGE"
    )

async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /access CODE")
        return

    code = context.args[0]
    user_id = str(update.effective_user.id)

    if code not in codes:
        await update.message.reply_text("Invalid code")
        return

    users[user_id] = ""
    codes.remove(code)

    with open("users.json", "w") as f:
        json.dump(users, f)

    with open("codes.json", "w") as f:
        json.dump(codes, f)

    await update.message.reply_text("Access granted ✅\nNow use /setmsg")

async def setmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in users:
        await update.message.reply_text("No access ❌")
        return

    if not context.args:
        await update.message.reply_text("Use: /setmsg your message")
        return

    users[user_id] = " ".join(context.args)

    with open("users.json", "w") as f:
        json.dump(users, f)

    await update.message.reply_text("Message saved ✅")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective
