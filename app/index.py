from flask import Flask, request, jsonify
from validations import validate_input_data

app = Flask(__name__)

@app.route('/status-check')
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
    
    # Return the processed list
    return jsonify(processed_data), 200
