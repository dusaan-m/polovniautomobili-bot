# kupujemprodajem-bot

## Description:

This project aims to scrape the latest car listings from the website polovniautomobili.com at regular intervals and send
notifications of new listings to a user via Telegram bot. By automating this process, users can stay updated on the
latest additions to the website without having to manually check it.

## Features:

- Web scraping of polovniautomobili.com to retrieve the latest car listings.
- Integration with a Telegram bot to send notifications of new listings.
- Automation of the scraping process to run every two hours.
- Ability to customize the frequency of scraping and other parameters.

## Dependencies:

- Python >3.11
- python-telegram-bot
- playwright
- apscheduler
- python-dotenv
- loguru

## Installation:

1. Clone the repository from GitHub: `git clone https://github.com/dusaan-m/kupujemprodajem-bot.git`
2. Navigate to the project directory: `cd kupujemprodajem-bot`
3. Create a virtual environment: `python -m venv venv`
4. Install the required dependencies using pip: `pip install -r requirements.txt`

## Usage:

1. Change .env.example to .env and fill in Telegram API token obtained from BotFather.
2. Run the main script: `python main.py`
3. Navigate to telegram and start conversation with the bot and send him the link of search made on
   polovniautomobili.com
4. The script will scrape the website for new car listings and send notifications to the Telegram bot.

## Contributing:

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a
pull request on GitHub.

## License:

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact:

For any inquiries or support, please contact [milivojevic.d@proton.me](mailto:milivojevic.d@proton.me)

## Disclaimer:

This project is for educational purposes only. Use it responsibly and ensure compliance with the terms of service of the
scraped website.
