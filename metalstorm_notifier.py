import random
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

# دیتابیس ساده برای ثبت کاربران
sent_greetings = set()

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in sent_greetings:
        greetings = ["سلام 😊", "درود 👋", "سلام رفیق 😎", "خوش اومدی 🌟", "های 👋", "سلام دوست من ❤️"]
        greeting_message = random.choice(greetings)
        context.bot.send_message(chat_id=user_id, text=greeting_message)
        sent_greetings.add(user_id)
    
    # ارسال وضعیت کد
    code = get_latest_code()  # تابعی که بررسی می‌کنه کد جدید هست یا نه
    if code:
        context.bot.send_message(chat_id=user_id, text=f"کد فعال جدید✅: {code}")
    else:
        context.bot.send_message(chat_id=user_id, text="فعلاً کد فعالی وجود ندارد.")

