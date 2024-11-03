from pymongo import MongoClient
from bson import json_util
import json
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
    query = {"url":url}
    result = collection.replace_one(query, data, upsert=True)

def parse_mongo_json(data):
    return json.loads(json_util.dumps(data))

def read(url):
    query = {"url":url}
    document = collection.find_one(query)
    return parse_mongo_json(document)
