import requests
import json
import random
import os
import time

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
CHAT_ID = '7554650927'
SENT_HELLO_FILE = 'hello_sent.json'
LAST_CODE_FILE = 'last_code.txt'

greetings = [
    "سلام دوست عزیز! 😊",
    "درود بر تو قهرمان! ⚔️",
    "خوش اومدی! 😎",
    "هی رفیق! 👋",
    "سلام! آماده‌ای؟ 🚀"
]

def send_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def send_greeting_once():
    if not os.path.exists(SENT_HELLO_FILE):
        greeting = random.choice(greetings)
        send_message(greeting)
        with open(SENT_HELLO_FILE, 'w') as f:
            json.dump({'sent': True}, f)

def fetch_codes_from_sources():
    """
    این تابع کدهای جدید رو از منابع مختلف می‌گیره.
    فعلاً نمونه اولیه فقط از Reddit پیاده‌سازی شده.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://www.reddit.com/r/MetalstormGame/new/.json', headers=headers, timeout=10)
        posts = response.json()['data']['children']
        codes = []
        for post in posts:
            title = post['data']['title']
            if 'code' in title.lower():
                codes.append(title.strip())
        return codes
    except Exception as e:
        print("خطا در دریافت کد:", e)
        return []

def get_last_sent_code():
    if os.path.exists(LAST_CODE_FILE):
        with open(LAST_CODE_FILE, 'r') as f:
            return f.read().strip()
    return ""

def save_last_sent_code(code):
    with open(LAST_CODE_FILE, 'w') as f:
        f.write(code)

def main():
    send_greeting_once()

    codes = fetch_codes_from_sources()
    if not codes:
        send_message("فعلاً کد فعالی وجود ندارد ❌")
        return

    last_code = get_last_sent_code()
    if codes[0] != last_code:
        send_message(f"کد فعال جدید ✅:\n\n{codes[0]}")
        save_last_sent_code(codes[0])
    else:
        send_message("فعلاً کد جدیدی منتشر نشده ❌")

if __name__ == '__main__':
    main()
