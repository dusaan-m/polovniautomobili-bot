import asyncio
from loguru import logger

from playwright.async_api import async_playwright, Page


class KPScraper:
    def __init__(self):
        self.headless = True
        self.scraped_cars: set[str] = set()

    @staticmethod
    def _headers():
        return {
            'Host': 'www.polovniautomobili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
        }

    async def scrape(self, url_to_cars: str) -> set[str]:
        logger.info(f"Scraping started for {url_to_cars}")
        page_num = 1
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=self.headless)
            page = await browser.new_page()
            await page.set_extra_http_headers(self._headers())
            await page.goto(url_to_cars)
            await self._scrape_cars(page)
            logger.info(f"Scraping page {page_num} finished")

            while await page.query_selector('.js-pagination-next'):
                page_num += 1
                await asyncio.sleep(15)
                await page.click('.js-pagination-next')
                await page.wait_for_load_state('load')
                await self._scrape_cars(page)
                logger.info(f"Scraping page {page_num} finished")

        logger.success(f"Scraping finished: {len(self.scraped_cars)} cars scraped")
        return self.scraped_cars

    async def _scrape_cars(self, page: Page):
        car_window = await page.query_selector('div.js-hide-on-filter:nth-child(3)')
        links = await car_window.query_selector_all('a')
        for link in links:
            if await link.is_visible():
                href = await link.get_attribute('href')
                if href and 'auto-oglasi' in href and "pretraga?" not in href:
                    href = href.split('?')[0]
                    self.scraped_cars.add(href)
