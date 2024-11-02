from flask import Flask, request, jsonify
from selenium_utils import capture_network_calls_headless, capture_network_calls_ui
from validations import validate_input_data
from mongo_utils import write

app = Flask(__name__)

@app.route('/status-check')
def hello():
    return 'true'

@app.route('/scrape/network', methods=['POST'])
def process_json_list():
    headless = request.args.get('headless', default="true", type=str)

    if not request.is_json:
        return jsonify({"error": "invalid input, JSON expected"}), 400
    
    data = request.get_json()
    processed_data = []

    try:
        processed_data = validate_input_data(data=data)
    except Exception as e:
        return jsonify({"error": repr(e)}), 400
    
    sample_url = processed_data[0]["url"]
    calls = []
    if (headless == "true"):
        print("using headless mode")
        calls = capture_network_calls_headless(sample_url)
    else:
        print("using ui mode")
        calls = capture_network_calls_ui(sample_url)
    
    write(url=sample_url, raw_data=calls)

    return jsonify(calls), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
