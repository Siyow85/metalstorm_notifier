import requests
import time
import random
from flask import Flask, request
from threading import Thread

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
app = Flask(__name__)

users = set()
sent_greeting = set()
latest_code = None

greetings = ['سلام 🌸', 'درود ✨', 'سلام رفیق 🤍', 'هَی 👋', 'چطوری 😎']

def get_new_code():
    sources = [
        'https://www.reddit.com/r/MetalstormGame/new.json?limit=5',
        # در آینده می‌توان منابع دیگر اضافه کرد (مانند APIهای دیسکورد و کانال‌های دیگر)
    ]
    headers = {'User-agent': 'Mozilla/5.0'}
    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            posts = r.json()['data']['children']
            for post in posts:
                title = post['data']['title']
                if 'code' in title.lower():
                    return title
        except Exception:
            continue
    return None

def send_message(chat_id, text):
    url = f'{API_URL}/sendMessage'
    requests.post(url, data={'chat_id': chat_id, 'text': text})

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def receive_update():
    global latest_code
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        users.add(chat_id)
        if text.lower() == '/start':
            if chat_id not in sent_greeting:
                greeting = random.choice(greetings)
                send_message(chat_id, greeting)
                sent_greeting.add(chat_id)
            if latest_code:
                send_message(chat_id, f'کد فعال جدید✅\n{latest_code}')
            else:
                send_message(chat_id, 'فعلاً کد فعالی وجود ندارد 🤍')
    return 'OK'

def poll_new_codes():
    global latest_code
    while True:
        code = get_new_code()
        if code and code != latest_code:
            latest_code = code
            for user in users:
                send_message(user, f'کد فعال جدید✅\n{latest_code}')
        time.sleep(60)

def run_bot():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=poll_new_codes).start()
    run_bot()
