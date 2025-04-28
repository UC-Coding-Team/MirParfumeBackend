# utils/telegram.py

import requests

TELEGRAM_TOKEN = 'TOKEN'
CHAT_ID = 'СHAT_ID'  

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        print(f"Ошибка отправки сообщения в Telegram: {response.text}")
