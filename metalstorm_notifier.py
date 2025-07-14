import requests
import time
import random
import os

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# پیام‌های خوش‌آمدگویی رندوم
GREETINGS = [
    "سلام 👋",
    "درود بر تو ✨",
    "خوش اومدی 😄",
    "هی رفیق! 👊",
    "سلام قهرمان 💪",
    "سلام به Metalstorm‌باز حرفه‌ای! 🚀",
    "سلااام 😎",
    "خوش اومدی به ربات کدت یاب 🔍",
]

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates["ok"] and updates["result"]:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    text = message.get("text", "")
                    if text == "/start":
                        greeting = random.choice(GREETINGS)
                        send_message(chat_id, greeting)

        time.sleep(1)

if __name__ == "__main__":
    main()
