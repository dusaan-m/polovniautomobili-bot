import asyncio
from loguru import logger
import json

from telegram import Bot

from kupujemprodajem_scrape import KPScraper


async def send_new_cars_message(bot: Bot, chat_id, url_to_cars, scraped_cars: set[str]):
    kp_link = "https://www.polovniautomobili.com"
    chat_id = str(chat_id)

    with open('users.json', 'r') as user_file:
        user_data = json.load(user_file)

    user_data[chat_id] = user_data.get(chat_id, {})

    if user_data[chat_id].get("url") != url_to_cars:
        user_data[chat_id]["url"] = url_to_cars
        user_data[chat_id]["cars"] = list(scraped_cars)
    else:
        old_cars = set(user_data[chat_id]["cars"])
        new_cars = scraped_cars - old_cars

        if not new_cars:
            await bot.send_message(chat_id, "Nema novih automobila")
        else:
            await bot.send_message(chat_id, f"Novi automobili:")
            for car in new_cars:
                logger.success(f"{chat_id}: {car}")
                await bot.send_message(chat_id, f"{kp_link}{car}")
                await asyncio.sleep(1)

        user_data[chat_id]["cars"] = list(new_cars | old_cars)

    with open('users.json', 'w') as user_file:
        json.dump(user_data, user_file, indent=4)


async def scrape_and_send_message(bot: Bot, chat_id, url_to_cars):
    logger.info(f"Scraping started url: {url_to_cars}")
    scraper = KPScraper()
    scraped_cars = await scraper.scrape(url_to_cars)
    logger.success(f"Scraping finished url: {url_to_cars}")

    logger.info(f"Sending new cars to user {chat_id}")
    await send_new_cars_message(bot, chat_id, url_to_cars, scraped_cars)
    logger.success(f"Sending finished for user {chat_id}")
