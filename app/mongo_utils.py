from pymongo import MongoClient
import time

mongo_client = MongoClient("mongodb://admin:password@mongo:27017/")
db = mongo_client["scrapper"]
collection = db["network_data"]

def write(url, raw_data):
    data = {
        "url": url,
        "data": raw_data,
        "ts": int(time.time() * 1000)
    }
    result = collection.insert_one(data)

def read(url):
    pass