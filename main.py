import os
import asyncio
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

# === 環境變數 ===
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TRADER_UID = os.environ["TRADER_UID"]

bot = Bot(token=TELEGRAM_TOKEN)

last_trade_text = ""

# === 建立 headless Selenium 瀏覽器 ===
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    return webdriver.Chrome(options=chrome_options)

# === 檢查 Binance Copy Trading 頁面 ===
def fetch_latest_record():
    url = f"https://www.binance.com/en/copy-trading/lead-details/{TRADER_UID}?timeRange=30D"
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(5)  # 等待網頁載入，視情況調整

        # 根據網頁中的「Latest Records」區塊的內容進行定位（此處視具體頁面調整）
        elems = driver.find_elements("css selector", "div.css-1jj2b1a")  # ⚠️ 請根據實際 class 名修正
        if elems:
            latest = elems[0].text.strip()
            return latest
        else:
            return None
    except Exception as e:
        return f"[錯誤] {e}"
    finally:
        driver.quit()

# === 檢查是否有新交易紀錄 ===
async def check_and_notify():
    global last_trade_text
    result = fetch_latest_record()

    if result is None:
        print("📭 無法取得最新交易紀錄")
        return

    if result.startswith("[錯誤]"):
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ 程式錯誤：{result}")
        return

    if result != last_trade_text:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"📈 新交易紀錄：\n{result}")
        last_trade_text = result
    else:
        print("⏳ 無新交易，等待下一輪檢查")

# === 主循環 ===
async def monitor_loop():
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ Binance CopyTrade 監控已啟動")
    while True:
        await check_and_notify()
        await asyncio.sleep(60)  # 每分鐘檢查一次

# === 執行程式 ===
if __name__ == "__main__":
    asyncio.run(monitor_loop())
