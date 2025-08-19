import telebot
import time
import threading
import requests
from flask import Flask
import os
from datetime import datetime

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
        url = "https://api.bybit.com/spot/v1/symbols"
        r = requests.get(url, timeout=10)
        data = r.json()
        symbols = [s.get("name") for s in data.get("result", []) if "name" in s]

        if "DEXNETUSDT" in symbols:
            try:
                price_url = "https://api.bybit.com/spot/quote/v1/ticker/price?symbol=DEXNETUSDT"
                price_resp = requests.get(price_url, timeout=10).json()
                price = price_resp.get("price", "неизвестно")
                msg = f"✅ Монета *DEXNET* появилась на бирже *Bybit*.\n💰 Цена сейчас: {price} $"
            except:
                msg = "✅ Монета *DEXNET* появилась на бирже *Bybit*, но цену пока не удалось получить."
        else:
            msg = "❌ Монета *DEXNET* ещё не появилась на бирже *Bybit*."
        return msg
    except:
        return "❌ Монета *DEXNET* ещё не появилась на бирже *Bybit*."

def send_price_loop():
    # сразу отправляем уведомление при старте
    text = check_bybit()
    try:
        bot.send_message(CHAT_ID, text, parse_mode="Markdown")
    except Exception as e:
        print("Ошибка при отправке:", e)

    while True:
        now = datetime.now()
        # считаем, сколько секунд до следующего часа ровно
        seconds_to_next_hour = (60 - now.minute) * 60 - now.second
        time.sleep(seconds_to_next_hour)

        # отправляем уведомление ровно в начале часа
        text = check_bybit()
        try:
            bot.send_message(CHAT_ID, text, parse_mode="Markdown")
        except Exception as e:
            print("Ошибка при отправке:", e)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=send_price_loop).start()
    bot.infinity_polling()
