import telebot
import time
import threading
import requests
from flask import Flask
import os

# --- Твои данные ---
TOKEN = "8196239170:AAFT9dNSP5iN8-zV6co8qyc2wVAYHFCmWc8"
CHAT_ID = "1718901610"

bot = telebot.TeleBot(TOKEN)

# --- Flask сервер для Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- Проверка монеты на Bybit ---
def check_bybit():
    try:
        url = "https://api.bybit.com/v2/public/tickers?symbol=DEXNETUSDT"
        r = requests.get(url, timeout=10)
        data = r.json()

        if data.get("retCode") == 0 and data.get("result"):
            price = data["result"][0].get("lastPrice")
            if price:
                return f"🚀 DEXNET появилась на Bybit! Текущая цена: {price} $"
            else:
                return "DEXNET появилась на Bybit, но цена пока недоступна."
        else:
            return "Монета DEXNET пока не появилась на бирже Bybit."
    except Exception as e:
        return f"Ошибка при проверке Bybit: {e}"

# --- Отправка уведомлений каждый час ---
def send_price_loop():
    while True:
        try:
            text = check_bybit()
            bot.send_message(CHAT_ID, text)
        except Exception as e:
            print("Ошибка при отправке:", e)
        time.sleep(3600)  # каждый час

# --- Стартуем всё ---
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()       # Flask для Render
    threading.Thread(target=send_price_loop).start()  # уведомления
    bot.infinity_polling()
