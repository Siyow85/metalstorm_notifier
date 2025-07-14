import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
CHAT_ID = '7554650927'
REDDIT_URL = 'https://www.reddit.com/r/MetalstormGame/new/'

HEADERS = {'User-Agent': 'Mozilla/5.0'}
SENT_CODES = set()

# پیام تستی بعد از اجرای بات
def send_test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "✅ بات با موفقیت در Railway اجرا شد و فعاله!"}
    requests.post(url, data=payload)

# ارسال پیام به تلگرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

# بررسی کدهای جدید در Reddit
def check_for_codes():
    try:
        response = requests.get(REDDIT_URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('h3')
        for title in titles:
            text = title.get_text()
            if "code" in text.lower() or "redeem" in text.lower():
                if text not in SENT_CODES:
                    SENT_CODES.add(text)
                    send_to_telegram(f"🎮 کد جدید پیدا شد:\n\n{text}")
    except Exception as e:
        print("خطا:", e)

if __name__ == "__main__":
    send_test_message()
    while True:
        check_for_codes()
        time.sleep(300)  # هر 5 دقیقه چک می‌کنه
