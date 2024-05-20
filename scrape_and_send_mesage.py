import asyncio

from loguru import logger
from telegram import Bot

from database import user_db, User
from kupujemprodajem_scrape import KPScraper


async def send_new_cars(bot: Bot, chat_id, new_cars: set[str]):
    kp_link = "https://www.polovniautomobili.com"

    await bot.send_message(chat_id, f"Novi automobili:")

    logger.info(f"{chat_id}: Sending {len(new_cars)} new cars to user")
    for car in new_cars:
        logger.success(f"{chat_id}: {car}")
        await bot.send_message(chat_id, f"{kp_link}{car}")
        await asyncio.sleep(1)


async def send_no_new_cars(bot: Bot, chat_id):
    logger.info(f"{chat_id}: No new cars")
    await bot.send_message(chat_id, "Nema novih automobila")


async def send_message(bot: Bot, chat_id, url_to_cars, scraped_cars: set[str]):
    logger.info(f"Sending new cars to user {chat_id}")
    chat_id = str(chat_id)
    user: User = user_db.get_user(chat_id)

    url_changed = user.url != url_to_cars
    if url_changed:
        user.url = url_to_cars
        user.cars = list(scraped_cars)
        user_db.update_url(chat_id, url_to_cars)
    else:
        old_cars = set(user.cars)
        new_cars = scraped_cars.difference(old_cars)

        if new_cars:
            await send_new_cars(bot, chat_id, new_cars)
        else:
            await send_no_new_cars(bot, chat_id)

        old_cars.update(new_cars)
        user.cars = list(old_cars)

    user_db.update_cars(chat_id, user.cars)

    logger.success(f"Sending finished for user {chat_id}")


async def scrape_and_send_message(bot: Bot, chat_id, url_to_cars):
    scraped_cars = await KPScraper().scrape(url_to_cars)

    await send_message(bot, chat_id, url_to_cars, scraped_cars)
