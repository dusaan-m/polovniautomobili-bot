import datetime
from loguru import logger
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scrape_and_send_mesage import scrape_and_send_message

scheduler = AsyncIOScheduler()
scheduler.start()


def re_add_jobs(bot):
    logger.info("Re-adding jobs")
    with open('users.json', 'r') as user_file:
        user_data = json.load(user_file)

    for user_id, data in user_data.items():
        if data.get("url"):
            logger.info(f"Re-adding job for user {user_id}")
            scheduler.add_job(scrape_and_send_message, id=user_id, trigger='interval', args=[bot, user_id, data["url"]],
                              hours=3, next_run_time=datetime.datetime.now())

    logger.success("Jobs re-added")


def add_job(bot, chat_id, url):
    logger.info(f"Adding job for user {chat_id}")

    chat_id = str(chat_id)
    if scheduler.get_job(chat_id):
        logger.info(f"Removing existing job for user {chat_id}")
        scheduler.remove_job(chat_id)

    scheduler.add_job(scrape_and_send_message, id=chat_id, trigger='interval', args=[bot, chat_id, url], hours=3,
                      next_run_time=datetime.datetime.now())

    logger.success(f"Job added for user {chat_id}")
