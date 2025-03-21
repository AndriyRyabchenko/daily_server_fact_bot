import os
import openai
import logging
from telegram import Bot
from dotenv import load_dotenv

# === Завантаження змінних з .env ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# === Налаштування логів ===
logging.basicConfig(
    filename='fact_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === Зчитування вже надісланих фактів ===
SENT_FACTS_FILE = "sent_facts.txt"
def is_fact_already_sent(fact):
    if not os.path.exists(SENT_FACTS_FILE):
        return False
    with open(SENT_FACTS_FILE, "r", encoding="utf-8") as f:
        return fact in f.read()

def save_fact(fact):
    with open(SENT_FACTS_FILE, "a", encoding="utf-8") as f:
        f.write(fact + "\n")

# === Отримання факту від OpenAI ===
def get_server_fact():
    openai.api_key = OPENAI_API_KEY
    prompt = (
        "Згенеруй один цікавий факт зі світу серверів, коротко, простою мовою, "
        "у стилі для публікації в Telegram-каналі. Максимум 50 слів. Без зайвого вступу, лише факт."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Помилка при запиті до OpenAI: {e}")
        return None

# === Надсилання в Telegram ===
def post_to_telegram(text):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=f"🖥️ Цікавий факт:\n\n{text}")
        logging.info(f"Факт надіслано: {text}")
    except Exception as e:
        logging.error(f"Помилка при надсиланні до Telegram: {e}")

# === Основна логіка ===
def main():
    fact = get_server_fact()
    if not fact:
        return

    if is_fact_already_sent(fact):
        logging.warning("Згенерований факт уже був раніше. Пропущено.")
        return

    post_to_telegram(fact)
    save_fact(fact)

if __name__ == "__main__":
    main()