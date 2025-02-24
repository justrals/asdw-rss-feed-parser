import pytz
import os
import feedparser
import asyncio
from telegram.ext import Application
from telegram.error import TimedOut
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

RSS_URL = "https://asdw.nbed.ca/alerts/feed/"

application = Application.builder().token(TELEGRAM_TOKEN).build()

last_alert_guid = None

halifax_tz = pytz.timezone('America/Halifax')


def convert_time_zone(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, "%a, %d %b %Y %H:%M:%S +0000")
    utc_time = pytz.utc.localize(utc_time)

    halifax_time = utc_time.astimezone(halifax_tz)

    return halifax_time.strftime('%Y-%m-%d %H:%M:%S')


async def send_alert_to_telegram(alert_message, alert_date, alert_link):
    halifax_date = convert_time_zone(alert_date)

    message = f"*{alert_message}*\n\n_{halifax_date}_\n\n[Read More]({alert_link})"
    try:
        await application.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        await asyncio.sleep(2)
    except TimedOut:
        print("Request timed out. Retrying...")
        await application.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')


async def scan_feed():
    global last_alert_guid
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        alert_message = entry.title
        alert_date = entry.published
        alert_link = entry.link
        alert_guid = entry.guid

        if alert_guid != last_alert_guid:
            await send_alert_to_telegram(alert_message, alert_date, alert_link)
            last_alert_guid = alert_guid


async def main():
    while True:
        await scan_feed()
        await asyncio.sleep(60 * 5)


if __name__ == '__main__':
    asyncio.run(main())
