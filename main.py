import scheduler
from kupujemprodajem_bot import app
from loguru import logger

scheduler.re_add_jobs(app.bot)
logger.info("Starting polling")
app.run_polling()
