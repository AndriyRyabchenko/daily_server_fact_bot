import os
import openai
import logging
from telegram import Bot
from dotenv import load_dotenv
from datetime import datetime

# === Завантаження змінних середовища ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# === Лог-файл ===
LOG_FILE = "sent_facts.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Генерація факту через OpenAI ===
def get_server_fact():
    openai.api_key = OPENAI_API_KEY
    prompt = (
        "Згенеруй один цікавий факт зі світу серверів, коротко і просто, у стилі для Telegram. "
        "Без привітання. Максимум 50 слів."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"❌ OpenAI error: {e}")
        return None

# === Відправка в Telegram ===
def send_to_telegram(fact):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=f"🖥️ Цікавий факт:\n\n{fact}")
        logging.info(f"✅ Надіслано факт: {fact}")
        return True
    except Exception as e:
        logging.error(f"❌ Telegram error: {e}")
        return False

# === Головна функція ===
def main():
    fact = get_server_fact()
    if not fact:
        logging.error("❌ Факт не згенеровано.")
        return

    success = send_to_telegram(fact)
    if not success:
        logging.warning(f"⚠️ Факт збережено локально через помилку: {fact}")

if __name__ == "__main__":
    main()