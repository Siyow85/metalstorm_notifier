from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests
import json
import os

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
DATA_FILE = 'users.json'  # برای ذخیره کاربرانی که استارت زدن
LAST_CODE_FILE = 'last_code.txt'  # برای ذخیره آخرین کد ارسال شده

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

def load_last_code():
    if os.path.exists(LAST_CODE_FILE):
        with open(LAST_CODE_FILE, 'r') as f:
            return f.read().strip()
    return ''

def save_last_code(code):
    with open(LAST_CODE_FILE, 'w') as f:
        f.write(code)

def fetch_latest_code():
    # اینجا باید کدهای جدید رو از سایت‌های رسمی و منابع مختلف بگیری
    # الان یه نمونه فرضی کد هست که در عمل باید API یا وبسایت‌ها رو پارس کنی
    # برای مثال فقط یه کد ثابت باز می‌گردونه:
    return "METALSTORM2025"

def start(update: Update, context: CallbackContext):
    users = load_users()
    chat_id = str(update.message.chat_id)
    if chat_id not in users:
        users.append(chat_id)
        save_users(users)

    keyboard = [[InlineKeyboardButton("کد Metalstorm", callback_data='metalstorm_code')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # فقط یکبار پیام خوش‌آمد بده
    if not context.user_data.get('started'):
        update.message.reply_text(
            'سلام! به ربات Metalstorm خوش آمدید. دکمه زیر را برای دریافت کدهای Metalstorm بزنید.',
            reply_markup=reply_markup)
        context.user_data['started'] = True
    else:
        # اگر قبلا استارت زده، فقط آخرین کد رو میفرسته
        last_code = load_last_code()
        if last_code:
            update.message.reply_text(f"آخرین کد Metalstorm: {last_code}", reply_markup=reply_markup)
        else:
            update.message.reply_text("فعلاً کد فعالی وجود ندارد 🤍", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'metalstorm_code':
        last_code = load_last_code()
        if last_code:
            query.edit_message_text(text=f"کد Metalstorm:\n{last_code}")
        else:
            query.edit_message_text(text="فعلاً کد فعالی وجود ندارد 🤍")

def notify_all_users(context: CallbackContext):
    users = load_users()
    latest_code = fetch_latest_code()
    last_code = load_last_code()

    if latest_code != last_code:
        save_last_code(latest_code)
        for chat_id in users:
            try:
                context.bot.send_message(chat_id=int(chat_id), text=f"کد فعال جدید Metalstorm ✅:\n{latest_code}")
            except Exception as e:
                print(f"خطا در ارسال پیام به {chat_id}: {e}")
    else:
        print("کد جدیدی برای ارسال نیست.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))

    # اجرای خودکار چک کردن کد جدید هر 5 دقیقه (300 ثانیه)
    job_queue = updater.job_queue
    job_queue.run_repeating(notify_all_users, interval=300, first=10)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
