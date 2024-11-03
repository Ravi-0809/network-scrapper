FROM python:3.11.3-slim

# Install Chromium, ChromeDriver, and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    openjdk-11-jre-headless \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download BrowserMob Proxy and extract it
RUN curl -L -o /tmp/browsermob-proxy.zip https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip \
    && unzip /tmp/browsermob-proxy.zip -d /opt \
    && rm /tmp/browsermob-proxy.zip

# Set environment variables for Chrome and ChromeDriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

WORKDIR /usr/src/network-scrapper
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/network-scrapper"
COPY . .
RUN pip install --no-cache-dir -r job/requirements.txt

# run script
CMD ["python", "-m", "job.selenium_job"]
