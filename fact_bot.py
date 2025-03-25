import os
import logging
import asyncio
from openai import OpenAI
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

LOG_FILE = "fact_bot.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_server_fact():
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": "Згенеруй один цікавий, технічно достовірний факт зі світу серверів. Без вигадки, лише правдиві дані. Стисло, зрозуміло, до 50 слів. Без привітання, без звертань, без жартів. Максимальна точність і логіка."
            }],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"❌ OpenAI error: {e}")
        return None

async def send_to_telegram(fact):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=f"🖥️ Цікавий факт:\n\n{fact}")
        logging.info(f"✅ Надіслано факт: {fact}")
        return True
    except Exception as e:
        logging.error(f"❌ Telegram error: {e}")
        return False

def main():
    fact = get_server_fact()
    if not fact:
        logging.error("❌ Факт не згенеровано.")
        return

    asyncio.run(send_to_telegram(fact))

if __name__ == "__main__":
    main()