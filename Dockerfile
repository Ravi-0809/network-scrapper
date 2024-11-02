FROM python:3.11.3-slim

# Install Chromium, ChromeDriver, and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    xvfb \
    libfontconfig1 \
    libxrender1 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome and ChromeDriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

WORKDIR /usr/src/network-scrapper
COPY . .
RUN pip install --no-cache-dir -r app/requirements.txt
EXPOSE 5000
ENV FLASK_APP=app/index.py
ENV FLASK_ENV=development

# Set the display environment variable for Xvfb
ENV DISPLAY=:99

# Run Xvfb in the background, then start Flask
CMD Xvfb :99 -screen 0 1920x1080x24 & flask run --host=0.0.0.0
