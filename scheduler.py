import datetime
import json
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.util import undefined
from loguru import logger

from database import user_db, User
from scrape_and_send_mesage import scrape_and_send_message

scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 15 * 60})
scheduler.start()


def re_add_jobs(bot):
    logger.info("Re-adding jobs")
    users: list[User] = user_db.get_all_users()

    for user in users:
        user_id = str(user.user_id)
        if user.url and user.run:
            logger.info(f"Re-adding job for user {user_id}")
            scheduler.add_job(scrape_and_send_message, id=user_id, trigger='interval', args=[bot, user_id, user.url],
                              hours=int(os.getenv("SCRAPE_INTERVAL_HOURS")),
                              next_run_time=datetime.datetime.now())

    logger.success("Jobs re-added")


def add_job(bot, chat_id, url, resume=False):
    logger.info(f"Adding job for user {chat_id}")

    chat_id = str(chat_id)
    user_db.update_run(chat_id, True)

    if scheduler.get_job(chat_id):
        logger.info(f"Removing existing job for user {chat_id}")
        scheduler.remove_job(chat_id)

    next_run_time = datetime.datetime.now() if not resume else undefined

    scheduler.add_job(scrape_and_send_message, id=chat_id, trigger='interval', args=[bot, chat_id, url],
                      hours=int(os.getenv("SCRAPE_INTERVAL_HOURS")),
                      next_run_time=next_run_time)

    logger.success(f"Job added for user {chat_id}")
