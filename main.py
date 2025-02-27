import os
import json
import pytz
import feedparser
import asyncio
from telegram.ext import Application
from telegram.error import TimedOut
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

application = Application.builder().token(TELEGRAM_TOKEN).build()

SENT_GUIDS_FILE = 'sent_guids.json'
halifax_tz = pytz.timezone('America/Halifax')


def load_sent_guids():
    if os.path.exists(SENT_GUIDS_FILE):
        with open(SENT_GUIDS_FILE, 'r') as file:
            return json.load(file)
    return []


def save_sent_guids(guids):
    with open(SENT_GUIDS_FILE, 'w') as file:
        json.dump(guids, file)


def add_sent_guid(guid):
    sent_guids = load_sent_guids()
    if guid not in sent_guids:
        sent_guids.append(guid)
        save_sent_guids(sent_guids)

def remove_first_sent_guid():
    sent_guids = load_sent_guids()
    if sent_guids:
        sent_guids.pop(0)
        save_sent_guids(sent_guids)

def extract_guid_number(guid_url):
    return guid_url.split('p=')[1]


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
    except Exception as e:
        print(f"Failed to send message: {e}")


async def scan_feed():
    sent_guids = load_sent_guids()
    feed = feedparser.parse('https://asdw.nbed.ca/alerts/feed/')

    for entry in reversed(feed.entries):
        alert_message = entry.title
        alert_date = entry.published
        alert_link = entry.link
        alert_guid = entry.guid

        guid_number = extract_guid_number(alert_guid)

        if guid_number not in sent_guids:
            await send_alert_to_telegram(alert_message, alert_date, alert_link)
            add_sent_guid(guid_number)
            remove_first_sent_guid()



async def main():
    while True:
        await scan_feed()
        await asyncio.sleep(60 * 5)


if __name__ == '__main__':
    asyncio.run(main())
