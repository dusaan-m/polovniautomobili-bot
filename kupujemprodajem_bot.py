import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from loguru import logger

import scheduler

load_dotenv()
API_TOKEN = os.getenv("BOT_API_TOKEN")


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Posalji mi link ka pretrazi kupujemprodajem")


async def scrape_kp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    scheduler.add_job(app.bot, update.message.chat.id, url)
    logger.info(f"Message recieved: {url}")
    await update.message.reply_text("Uspesno")


app = ApplicationBuilder().token(API_TOKEN).build()

app.add_handler(CommandHandler('start', send_welcome))
app.add_handler(MessageHandler(filters.Regex(r'^https://www.polovniautomobili.com/auto-oglasi/pretraga?'), scrape_kp))
