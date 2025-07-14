from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import logging
import asyncio

# پیام‌های سلام رندوم
greetings = [
    "سلام رفیق 😎",
    "درود بر تو 👋",
    "خوش اومدی 🤍",
    "سلام عزیز دل 💙",
    "خوش برگشتی 🌟",
]

# ذخیره آی‌دی‌هایی که قبلاً خوش‌آمد گفتیم
welcomed_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in welcomed_users:
        welcomed_users.add(user_id)
        greeting = random.choice(greetings)
        await update.message.reply_text(greeting)

    # بررسی وجود کد فعال
    active_code = await get_latest_code()
    if active_code:
        await update.message.reply_text(f"کد فعال جدید ✅:\n{active_code}")
    else:
        await update.message.reply_text("فعلاً کد فعالی وجود ندارد 🤍")

# این تابع می‌تونه از منابع مختلف کد پیدا کنه
async def get_latest_code():
    # فعلاً حالت تستی — بعداً می‌تونی از Reddit و Discord یا سایت‌های دیگه چک کنی
    # return "ABC123"  # برای تست
    return None  # اگر هیچ کدی نباشه

def main():
    app = ApplicationBuilder().token("7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U").build()

    app.add_handler(CommandHandler("start", start))

    logging.basicConfig(level=logging.INFO)
    print("ربات در حال اجراست...")

    app.run_polling()

if __name__ == "__main__":
    main()
