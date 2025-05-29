FROM python:3.11-slim

# 安裝 Chrome 及 Selenium 依賴
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libappindicator1 libindicator7 \
    libasound2 libatk-bridge2.0-0 libgtk-3-0 xvfb && \
    rm -rf /var/lib/apt/lists/*

# 安裝 Chrome 瀏覽器
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# 安裝 pip 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
