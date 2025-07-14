import requests
import time
import random
import json
from datetime import datetime

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
USER_DATA_FILE = 'user_data.json'
LAST_CODE_FILE = 'last_code.txt'

GREETING_MESSAGES = [
    "سلام عزیز دل 🤍",
    "درود رفیق 👋",
    "سلام به گل خوش اومدی 🌸",
    "درود جنگجو 🔥",
    "سلام قهرمان 🛡️",
]

# ----------------------- ابزار ذخیره‌سازی -----------------------
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f)

def load_last_code():
    try:
        with open(LAST_CODE_FILE, 'r') as f:
            return f.read().strip()
    except:
        return ''

def save_last_code(code):
    with open(LAST_CODE_FILE, 'w') as f:
        f.write(code)

# ----------------------- ارسال پیام -----------------------
def send_message(chat_id, text):
    requests.post(API_URL + 'sendMessage', data={'chat_id': chat_id, 'text': text})

# ----------------------- بررسی سایت‌ها -----------------------
def fetch_code_sources():
    codes = []

    # مثال از Reddit
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get('https://www.reddit.com/r/MetalstormGame/new.json', headers=headers)
        posts = r.json()['data']['children']
        for post in posts:
            title = post['data']['title']
            if "code" in title.lower() or "redeem" in title.lower():
                codes.append(title.strip())
    except:
        pass

    # مثال دیگر: Pastebin
    try:
        r = requests.get("https://pastebin.com/raw/metalstorm")
        lines = r.text.splitlines()
        for line in lines:
            if len(line.strip()) > 6:
                codes.append(line.strip())
    except:
        pass

    return codes

# ----------------------- مدیریت /start -----------------------
def handle_start(chat_id):
    users = load_user_data()
    last_code = load_last_code()

    if chat_id not in users:
        greeting = random.choice(GREETING_MESSAGES)
        send_message(chat_id, greeting)
        users[chat_id] = {"started": True}
        save_user_data(users)

    if last_code:
        send_message(chat_id, f"کد فعال فعلی:\n\n{last_code}")
    else:
        send_message(chat_id, "فعلاً کد فعالی وجود ندارد 🤍")

# ----------------------- بررسی آپدیت ها و دریافت پیام جدید -----------------------
def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(API_URL + 'getUpdates', params=params)
    return response.json()['result']

# ----------------------- حلقه اصلی -----------------------
def main():
    print("🤖 ربات در حال اجراست...")
    offset = None
    last_code = load_last_code()

    while True:
        # دریافت پیام های تلگرام
        updates = get_updates(offset)
        for update in updates:
            offset = update['update_id'] + 1
            if 'message' in update:
                chat_id = str(update['message']['chat']['id'])
                text = update['message'].get('text', '').lower()
                if text == '/start':
                    handle_start(chat_id)

        # بررسی کدهای جدید
        new_codes = fetch_code_sources()
        for code in new_codes:
            if code != last_code:
                print(f"کد جدید یافت شد: {code}")
                users = load_user_data()
                for user_id in users.keys():
                    send_message(user_id, f"کد فعال جدید ✅:\n\n{code}")
                last_code = code
                save_last_code(code)
        time.sleep(60)
