import telebot
import time
import threading
import requests
from flask import Flask
import os

TOKEN = "8196239170:AAFT9dNSP5iN8-zV6co8qyc2wVAYHFCmWc8"
CHAT_ID = "1718901610"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def check_bybit():
    try:
        # Получаем список всех спотовых символов
        url = "https://api.bybit.com/spot/v1/symbols"
        r = requests.get(url, timeout=10)
        data = r.json()

        symbols = [s.get("name") for s in data.get("result", []) if "name" in s]

        if "DEXNETUSDT" in symbols:
            # Монета есть, получаем цену
            try:
                price_url = "https://api.bybit.com/spot/quote/v1/ticker/price?symbol=DEXNETUSDT"
                price_resp = requests.get(price_url, timeout=10).json()
                price = price_resp.get("price", "неизвестно")
                return f"🚀 DEXNET появилась на Bybit! Текущая цена: {price} $"
            except:
                return "DEXNET появилась на Bybit, но цену получить не удалось."
        else:
            # Монеты нет
            return "Монета DEXNET пока не появилась на бирже Bybit."
    except:
        return "Монета DEXNET пока не появилась на бирже Bybit."

def send_price_loop():
    while True:
        text = check_bybit()
        try:
            bot.send_message(CHAT_ID, text)
        except Exception as e:
            print("Ошибка при отправке:", e)
        time.sleep(3600)  # каждый час

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=send_price_loop).start()
    bot.infinity_polling()
