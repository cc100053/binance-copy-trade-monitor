import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 環境變數
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TRADER_UID = os.environ.get("TRADER_UID")

# 初始化 Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)

def check_latest_trade():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://www.binance.com/en/copy-trading/lead-details/{TRADER_UID}?timeRange=30D"
        driver.get(url)
        time.sleep(5)  # 等待頁面加載

        # 在此處添加解析頁面內容的邏輯
        # 例如，檢查最新的交易記錄

        # 如果有新交易，發送 Telegram 通知
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="📈 檢測到新交易！")

    except Exception as e:
        logging.error(f"發生錯誤：{e}")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ 發生錯誤：{e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        check_latest_trade()
        time.sleep(60)  # 每分鐘檢查一次
