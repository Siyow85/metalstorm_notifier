import requests
import time
import random
import json
from datetime import datetime

BOT_TOKEN = 'توکن شما'
CHAT_ID = 'چت آیدی شما'

# سلام‌ رندوم با ایموجی
greetings = [
    "سلام دوست من! 👋",
    "درود بر تو! ✨",
    "خوش اومدی قهرمان! 🚀",
    "سلام به جنگجوی فلزی! 🤖",
    "هی، وقت کد جدیده؟ 🔥",
]

last_sent_code_file = "last_code.txt"

# سایت‌هایی که باید بررسی شوند
def fetch_codes_from_sources():
    codes = []

    # Reddit
    try:
        reddit = requests.get("https://www.reddit.com/r/MetalstormGame/new.json", headers={'User-agent': 'Mozilla/5.0'})
        posts = reddit.json()['data']['children']
        for post in posts:
            title = post['data']['title']
            if "code" in title.lower():
                codes.append(title.strip())
    except Exception as e:
        print("Reddit error:", e)

    # سایت دوم (مثال: پیج X سابق یا سایت دیگر)
    # try:
    #     response = requests.get("https://...")
    #     ... بررسی محتوا و اضافه کردن کدها به لیست codes
    # except:
    #     pass

    return codes

def get_last_sent_code():
    try:
        with open(last_sent_code_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def set_last_sent_code(code):
    with open(last_sent_code_file, "w") as f:
        f.write(code)

# ارسال پیام به کاربر
def send_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)

# بررسی اینکه پیام /start فرستاده شده یا نه
def check_start():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    res = requests.get(url)
    updates = res.json().get("result", [])

    for update in updates[::-1]:
        message = update.get("message", {})
        text = message.get("text", "").lower()
        if text == "/start":
            user_id = message["chat"]["id"]
            return user_id
    return None

# بررسی و ارسال کد جدید
def check_and_send_code():
    codes = fetch_codes_from_sources()
    if not codes:
        send_message("فعلاً کد فعالی وجود ندارد 🤍")
        return

    latest_code = codes[0]
    last_sent_code = get_last_sent_code()

    if latest_code != last_sent_code:
        send_message(f"کد فعال جدید ✅:\n\n{latest_code}")
        set_last_sent_code(latest_code)
    else:
        send_message(f"آخرین کد فعال:\n{latest_code}")

# اجرای دائمی ربات
def run_bot():
    greeted = False
    while True:
        user_id = check_start()
        if user_id and not greeted:
            greeting = random.choice(greetings)
            send_message(greeting)
            check_and_send_code()
            greeted = True
        time.sleep(30)  # هر ۳۰ ثانیه بررسی کند
