import os

from dotenv import load_dotenv
from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

import scheduler
from database import user_db, User

load_dotenv()
API_TOKEN = os.getenv("BOT_API_TOKEN")


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Start command recieved from {update.message.chat.id}")
    await update.message.reply_text("Posalji mi link ka pretrazi kupujemprodajem")


async def scrape_kp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    url = update.message.text
    logger.info(f"Message recieved: {url}")

    if not user_db.get_user(user_id):
        user = User(user_id=user_id, url=url, run=True, cars=[])
        user_db.add_user(user)

    scheduler.add_job(app.bot, user_id, url)
    await update.message.reply_text("Uspesno")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Stop command recieved from {update.message.chat.id}")

    # pause job if it exists
    if scheduler.scheduler.get_job(str(update.message.chat.id)):
        scheduler.scheduler.pause_job(str(update.message.chat.id))

    user_db.update_run(update.message.chat.id, False)

    logger.success(f"Job removed and stopped for user {update.message.chat.id}")
    await update.message.reply_text("Uspesno")


async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Resume command recieved from {update.message.chat.id}")
    user: User = user_db.get_user(update.message.chat.id)
    user_db.update_run(user.user_id, True)

    # resume job if it exists
    if scheduler.scheduler.get_job(str(user.user_id)):
        logger.info(f"Resuming job for user {user.user_id}")
        scheduler.scheduler.resume_job(str(user.user_id))
        await update.message.reply_text("Uspesno")
    else:
        if user.url:
            scheduler.add_job(app.bot, user.user_id, user.url)
            await update.message.reply_text("Uspesno")
        else:
            await update.message.reply_text("Nemate aktivnu pretragu, posaljite link ka pretrazi kupujemprodajem")


app = ApplicationBuilder().token(API_TOKEN).build()

app.add_handler(CommandHandler('start', send_welcome))
app.add_handler(CommandHandler('stop', stop))
app.add_handler(CommandHandler('resume', resume))
app.add_handler(MessageHandler(filters.Regex(r'^https://www.polovniautomobili.com/auto-oglasi/pretraga?'), scrape_kp))
