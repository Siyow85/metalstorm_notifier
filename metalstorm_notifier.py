import requests
from bs4 import BeautifulSoup
import re
import time
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# ======= توکن ربات خودت رو اینجا جایگزین کن ========
BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'

# فایل ذخیره شناسه کاربران و آخرین کد
USERS_FILE = 'users.txt'
LAST_CODE_FILE = 'last_code.txt'

# تابع بارگذاری کاربران
def load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

# تابع ذخیره کاربر جدید
def save_user(chat_id):
    users = load_users()
    if chat_id not in users:
        users.add(chat_id)
        with open(USERS_FILE, 'a', encoding='utf-8') as f:
            f.write(str(chat_id) + '\n')

# بارگذاری آخرین کد ذخیره شده
def load_last_code():
    try:
        with open(LAST_CODE_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''

# ذخیره آخرین کد
def save_last_code(code):
    with open(LAST_CODE_FILE, 'w', encoding='utf-8') as f:
        f.write(code)

# استخراج کد از Reddit Metalstorm
def fetch_code_from_reddit():
    url = 'https://www.reddit.com/r/MetalstormGame/new/.json?limit=10'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        posts = data.get('data', {}).get('children', [])
        code_pattern = re.compile(r'\b[A-Z0-9]{6,12}\b')  # الگوی ساده کد

        for post in posts:
            title = post['data'].get('title', '')
            selftext = post['data'].get('selftext', '')
            for text in [title, selftext]:
                codes = code_pattern.findall(text)
                if codes:
                    return codes[0]
    except Exception as e:
        print(f"Error fetching from reddit: {e}")
    return None

# استخراج کد از سایت رسمی Metalstorm (صفحه promotions)
def fetch_code_from_official_site():
    url = 'https://metalstormgame.com/promotions'
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        # فرض: کد داخل تگ span با کلاس promo-code است
        code_span = soup.find('span', class_='promo-code')
        if code_span:
            code = code_span.get_text(strip=True)
            return code
    except Exception as e:
        print(f"Error fetching from official site: {e}")
    return None

# بررسی کد جدید و ارسال پیام به کاربران
def check_and_send(updater: Updater):
    print("Checking for new Metalstorm codes...")
    sources = [fetch_code_from_reddit, fetch_code_from_official_site]
    new_code = None
    for source in sources:
        code = source()
        if code:
            new_code = code
            break

    if new_code:
        last_code = load_last_code()
        if new_code != last_code:
            print(f"New code found: {new_code}")
            save_last_code(new_code)
            users = load_users()
            for user in users:
                try:
                    updater.bot.send_message(
                        chat_id=user,
                        text=f"کد فعال جدید Metalstorm ✅:\n\n`{new_code}`",
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    print(f"Error sending to {user}: {e}")
        else:
            print("No new code found.")
    else:
        print("No code fetched from any source.")

    # هر 5 دقیقه چک می‌کنه
    threading.Timer(300, check_and_send, args=(updater,)).start()

# هندلر دستور /start
def start(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    save_user(chat_id)

    keyboard = [[InlineKeyboardButton("کد Metalstorm 🎮", callback_data='metalstorm_code')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    last_code = load_last_code()
    greeting = "سلام! برای دریافت آخرین کد Metalstorm روی دکمه زیر بزن:"
    update.message.reply_text(greeting, reply_markup=reply_markup)

    if last_code:
        update.message.reply_text(f"آخرین کد موجود:\n`{last_code}`", parse_mode='Markdown')
    else:
        update.message.reply_text("فعلاً کد فعالی وجود ندارد 🤍")

# هندلر کلیک دکمه
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'metalstorm_code':
        last_code = load_last_code()
        if last_code:
            query.edit_message_text(text=f"کد فعال Metalstorm:\n\n`{last_code}`", parse_mode='Markdown')
        else:
            query.edit_message_text(text="فعلاً کد فعالی وجود ندارد 🤍")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # شروع چک کردن کدها در پس‌زمینه
    check_and_send(updater)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("کد Metalstorm", callback_data='metalstorm_code')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('سلام! لطفا یک گزینه را انتخاب کن:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'metalstorm_code':
        # اینجا کد ارسال کدهای متال استورم را قرار بده
        query.edit_message_text(text="کد جدید Metalstorm: XYZ123")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

