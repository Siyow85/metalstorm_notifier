import requests
import random
import json
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, JobQueue

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
USERS_FILE = 'users.json'
GREETINGS = [
    "سلام! 🌟",
    "درود بر شما! 👋",
    "خوش آمدید! 😊",
    "سلام رفیق! ✌️",
    "سلام و روز بخیر! ☀️"
]

# ذخیره کاربران
def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def add_user(chat_id):
    users = load_users()
    if chat_id not in users:
        users.append(chat_id)
        save_users(users)

# تابع نمونه برای دریافت آخرین کد (باید جایگزین با کد واقعی بشه)
def get_last_code():
    # اینجا باید کدهای واقعی از سایت‌ها استخراج بشه
    # فعلا فقط نمونه می‌فرستم
    # اگر کدی نبود None برمی‌گردونه
    codes = ["METAL123", "METAL456", "METAL789"]  # نمونه
    return random.choice(codes) if random.random() > 0.5 else None

# تابع ارسال پیام خودکار به همه کاربران
def notify_users(context: CallbackContext):
    users = load_users()
    last_code = get_last_code()
    for user_id in users:
        if last_code:
            text = f"کد فعال جدید ✅:\n{last_code}"
        else:
            text = "فعلاً کد فعالی وجود ندارد 🤍"
        context.bot.send_message(chat_id=user_id, text=text)

# هندلر دستور /start
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    users = load_users()

    if str(chat_id) not in users:
        add_user(str(chat_id))
        greeting = random.choice(GREETINGS)
    else:
        greeting = "خوش برگشتی!"

    keyboard = [
        [InlineKeyboardButton("دریافت کد Metalstorm", callback_data='get_code')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat_id, text=greeting, reply_markup=reply_markup)

    # ارسال آخرین کد در پیام جداگانه
    last_code = get_last_code()
    if last_code:
        context.bot.send_message(chat_id=chat_id, text=f"آخرین کد فعال:\n{last_code}")
    else:
        context.bot.send_message(chat_id=chat_id, text="فعلاً کد فعالی وجود ندارد 🤍")

# هندلر کلیک دکمه
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'get_code':
        last_code = get_last_code()
        if last_code:
            text = f"آخرین کد فعال:\n{last_code}"
        else:
            text = "فعلاً کد فعالی وجود ندارد 🤍"
        query.edit_message_text(text=text)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # زمان‌بندی اجرای چک کردن کد هر 300 ثانیه (5 دقیقه)
    jq: JobQueue = updater.job_queue
    jq.run_repeating(notify_users, interval=300, first=10)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
