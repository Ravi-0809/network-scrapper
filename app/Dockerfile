FROM python:3.11.3-slim

# Install Chromium, ChromeDriver, and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome and ChromeDriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/network-scrapper"

WORKDIR /usr/src/network-scrapper
COPY . .
RUN pip install --no-cache-dir -r app/requirements.txt
EXPOSE 5000
ENV FLASK_APP=app/index.py
ENV FLASK_ENV=development

# start Flask
CMD flask run --host=0.0.0.0
