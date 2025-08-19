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

# --- Проверка монеты на Bybit через список спот-символов ---
def check_bybit():
    try:
        url = "https://api.bybit.com/spot/v1/symbols"
        r = requests.get(url, timeout=10)
        data = r.json()

        symbols = [item["name"] for item in data.get("result", [])]
        if "DEXNETUSDT" in symbols:
            # Получаем цену только если монета есть
            price_url = "https://api.bybit.com/spot/quote/v1/ticker/price?symbol=DEXNETUSDT"
            price_resp = requests.get(price_url, timeout=10).json()
            price = price_resp.get("price", "неизвестно")
            return f"🚀 DEXNET появилась на Bybit! Текущая цена: {price} $"
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
