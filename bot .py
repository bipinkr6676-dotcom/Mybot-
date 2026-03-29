from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from collections import defaultdict
import time

BOT_TOKEN = "8609410180:AAGmBD71Zr0DHKiuBP4RS0OcjBylaeAq2Yc"

user_messages = defaultdict(list)
SPAM_LIMIT = 5
SPAM_WINDOW = 5
warn_count = defaultdict(int)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Main tumhara group manager bot hun. /help dekho.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/kick\n/mute\n/unmute\n/warn\n/rules\n/help")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Rules:\n1. Respectful raho\n2. Spam mat karo\n3. NSFW nahi\n4. Admin suno")

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(user.first_name + " ko kick kar diya.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.restrict_chat_member(
            update.effective_chat.id, user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(user.first_name + " mute ho gaya.")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.restrict_chat_member(
            update.effective_chat.id, user.id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await update.message.reply_text(user.first_name + " unmute ho gaya.")

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        warn_count[user.id] += 1
        await update.message.reply_text("Warning " + user.first_name + " (" + str(warn_count[user.id]) + "/3)")
        if warn_count[user.id] >= 3:
            await context.bot.ban_chat_member(update.effective_chat.id, user.id)
            await update.message.reply_text(user.first_name + " ban ho gaya.")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text("Welcome " + member.first_name + "! /rules zaroor padho.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

print("Bot running...")
app.run_polling()
