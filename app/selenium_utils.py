from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import time

def capture_network_calls(url, username = None, password = None):
    network_calls = []
    options = webdriver.ChromeOptions()
    
    # Set logging preferences for network capture
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    
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