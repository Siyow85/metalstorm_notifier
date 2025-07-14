import requests
import time
import json
import os
import random
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
USERS_FILE = 'users.txt'
CHECK_INTERVAL = 300  # هر 5 دقیقه چک می‌کند

# لیست پیام‌های خوش آمد + ایموجی (یکی رندوم ارسال می‌شود)
GREETINGS = [
    "سلام 😊",
    "درود 🌟",
    "سلامتی 💚",
    "درود بر شما 🙌",
    "خوش آمدید 🤗",
]

def save_user(chat_id: int):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            pass
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        users = f.read().splitlines()
    if str(chat_id) not in users:
        with open(USERS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{chat_id}\n")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

# --- استخراج کد از سایت رسمی فرضی Metalstorm ---
def fetch_latest_code_metalstorm():
    url = 'https://metalstormgame.com/promocodes'  # لینک فرضی (لطفا اصلاح شود)
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        code_div = soup.find('div', class_='promo-code')
        if code_div:
            code = code_div.text.strip()
            return code
    except Exception as e:
        print(f"خطا در دریافت کد از سایت رسمی: {e}")
    return None

# --- استخراج کد از Reddit ---
def fetch_latest_code_reddit():
    url = 'https://www.reddit.com/r/MetalstormGame/new/.json?limit=5'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        for post in data['data']['children']:
            title = post['data']['title']
            if 'CODE' in title.upper():
                words = title.split()
                for w in words:
                    if len(w) >= 6 and w.isalnum():
                        return w.strip()
    except Exception as e:
        print(f"خطا در دریافت کد از Reddit: {e}")
    return None

# --- تابع اصلی گرفتن کد ---
def fetch_latest_code():
    code = fetch_latest_code_metalstorm()
    if code:
        return code
    code = fetch_latest_code_reddit()
    if code:
        return code
    return None

# ذخیره کد فعلی در فایل برای مقایسه و تشخیص کد جدید
CODE_FILE = 'last_code.txt'

def get_last_code():
    if os.path.exists(CODE_FILE):
        with open(CODE_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def save_last_code(code):
    with open(CODE_FILE, 'w', encoding='utf-8') as f:
        f.write(code)

# --- هندلر /start ---
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    users = load_users()
    if str(chat_id) not in users:
        save_user(chat_id)
        greeting = random.choice(GREETINGS)
        context.bot.send_message(chat_id=chat_id, text=greeting)

    # ارسال آخرین کد یا پیام "کد نیست"
    last_code = get_last_code()
    if last_code:
        context.bot.send_message(chat_id=chat_id, text=f"آخرین کد فعال: {last_code}")
    else:
        context.bot.send_message(chat_id=chat_id, text="فعلاً کد فعالی وجود ندارد 🤍")

# --- تابع اطلاع‌رسانی کد جدید به همه ---
def notify_all_users(context: CallbackContext, new_code):
    users = load_users()
    for user_id in users:
        try:
            context.bot.send_message(chat_id=int(user_id), text=f"کد فعال جدید ✅:\n{new_code}")
        except Exception as e:
            print(f"خطا در ارسال پیام به کاربر {user_id}: {e}")

# --- چک کردن دوره‌ای کد جدید ---
def check_for_new_codes(context: CallbackContext):
    new_code = fetch_latest_code()
    if new_code:
        last_code = get_last_code()
        if new_code != last_code:
            print(f"کد جدید پیدا شد: {new_code}")
            save_last_code(new_code)
            notify_all_users(context, new_code)
        else:
            print("کد جدیدی پیدا نشد.")
    else:
        print("کدی پیدا نشد.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    # اجرای چک دوره‌ای هر 5 دقیقه
    job_queue = updater.job_queue
    job_queue.run_repeating(check_for_new_codes, interval=CHECK_INTERVAL, first=10)

    updater.start_polling()
    print("بات شروع به کار کرد...")
    updater.idle()

if __name__ == '__main__':
    main()
