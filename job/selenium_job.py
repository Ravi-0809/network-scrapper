from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time
import argparse
from mongo.mongo_utils import write as writeToMongoDb
from urllib.parse import quote
from browsermobproxy import Server

driver_path = "/usr/bin/chromedriver"
# driver_path = "/opt/homebrew/bin/chromedriver"
proxy_path = "/opt/browsermob-proxy-2.1.4/bin/browsermob-proxy"


def capture_network_calls_headless(url, username = None, password = None):
    network_calls = []
    har_data = {}

    server = Server(proxy_path)
    server.start()
    proxy = server.create_proxy()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Necessary for running as root in Docker
    options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource issues
    options.add_argument("--disable-gpu")  # Disable GPU rendering (optional but useful in headless)
    options.add_argument("--remote-debugging-port=9222")  # Avoids the DevTools port issue
    options.add_argument(f'--proxy-server={proxy.proxy}')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-insecure-localhost')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    proxy.new_har(f"har_{url}", options={'captureHeaders': True, 'captureContent': True})

    updated_url = url
    if (username != None and password != None and username!= ""):
        base_url = ""
        if ("https://" in url):
            base_url = url.split("https://")[1]
        elif ("http://" in url):
            base_url = url.split("http://")[1]
        else:
            base_url = url
        updated_url = f"{quote(username)}:{quote(password)}@{base_url}"
    
    try:
        driver.get(updated_url)
        time.sleep(5) # wait 5 sec for all network calls
        har_data = proxy.har

        # logs = driver.get_log("performance")
        # requests = [json.loads(x["message"])["message"]["params"] for x in logs if "Network.responseReceived" in json.loads(x["message"])["message"]["method"]]
        # for param in requests:
        #     resp = param["response"] if "response" in param else ""
        #     url = resp["url"] if "url" in resp else ""
        #     status = resp["status"] if "status" in resp else ""
        #     if (url != ""):
        #         d = {"url": url, "status": status, "type": param['type']}
        #         network_calls.append(d)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        proxy.close()
        server.stop()
    driver.quit()
    proxy.close()
    server.stop()
    
    return har_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Network Scraper")
    parser.add_argument("url", help="url", type=str)
    parser.add_argument("--username", help="username", type=str)
    parser.add_argument("--password", help="url", type=str)

    # get args
    args = parser.parse_args()

    print(f"----- {args.url} -----")
    print(f"username = {args.username}")
    print(f"password = {args.password}")
    print("----------")
    print("----------")

    # get network calls using selenium
    har_data = capture_network_calls_headless(args.url, args.username, args.password)
    print("HAR capture complete")

    # write to db
    writeToMongoDb(url=args.url, raw_data=har_data)
    
    exit(0)


# ---- ui testing, ignore ----
def capture_network_calls_ui(url, username = None, password = None):
    network_calls = []
    options = Options()
    options.add_argument("--no-sandbox")  # Necessary for running as root in Docker
    options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource issues
    options.add_argument("--disable-gpu")  # Disable GPU rendering (optional but useful in headless)
    options.add_argument("--remote-debugging-port=9222")  # Avoids the DevTools port issue
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    service = Service(driver_path)
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=options
    )
    
    try:
        driver.get(url)

        while (driver.title):
            logs = driver.get_log("performance")
            requests = [json.loads(x["message"])["message"]["params"] for x in logs if "Network.responseReceived" in json.loads(x["message"])["message"]["method"]]
            for param in requests:
                resp = param["response"] if "response" in param else ""
                url = resp["url"] if "url" in resp else ""
                status = resp["status"] if "status" in resp else ""
                if (url != ""):
                    d = {"url": url, "status": status, "type": param['type']}
                    network_calls.append(d)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    driver.quit()
    return network_calls