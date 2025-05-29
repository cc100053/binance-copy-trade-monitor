FROM python:3.11-slim

# 安裝必要的套件
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# 建立工作目錄
WORKDIR /app

# 複製檔案
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 執行主程式
CMD ["python", "main.py"]
