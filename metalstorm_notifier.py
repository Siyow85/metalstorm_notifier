import random
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'

def start(update, context):
    greetings = [
        "سلام! 😊",
        "درود! 👋",
        "های! 😄",
        "سلام رفیق! ✌️",
        "سلام به شما 🌟",
        "چطوری؟ 🐱‍🏍",
        "هی سلام! 🚀"
    ]
    message = random.choice(greetings)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = '7737983627:AAGdTwXHkeGq3bTekUPbaBfrUHwt7x7gA9U'
CHAT_ID = '7554650927'
URL = 'https://www.reddit.com/r/MetalstormGame/new/'

headers = {'User-Agent': 'Mozilla/5.0'}
sent_posts = set()

def send_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def check_new_posts():
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        if '/r/MetalstormGame/comments/' in href and href not in sent_posts:
            sent_posts.add(href)
            full_url = f'https://www.reddit.com{href}' if href.startswith('/') else href
            send_message(f'🔥 New Post: {full_url}')

if __name__ == '__main__':
    while True:
        check_new_posts()
        time.sleep(300)
