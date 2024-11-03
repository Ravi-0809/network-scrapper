from flask import Flask, request, jsonify
from validations import validate_input_data, validate_get_query_input
from job_handler import create_jobs
from mongo.mongo_utils import read as readFromMongo

app = Flask(__name__)

@app.route('/')
def hello():
    return 'true'

@app.route('/scrape/network', methods=['POST'])
def process_json_list():
    if not request.is_json:
        return jsonify({"error": "invalid input, JSON expected"}), 400
    
    data = request.get_json()
    processed_data = []

    try:
        processed_data = validate_input_data(data=data)
    except Exception as e:
        return jsonify({"error": repr(e)}), 400
    
    create_jobs(processed_data=processed_data)

    return jsonify({"message": f"Scheduled {len(processed_data)} jobs successfully"}), 200

@app.route('/get/full', methods=['POST'])
def get_full_document():
    data = request.get_json()
    
    try:
        validate_get_query_input(data=data)
    except Exception as e:
        return jsonify({"error": repr(e)}), 400
    
    url = data["url"]
    doc = readFromMongo(url=url)
    
    return jsonify(doc), 200  