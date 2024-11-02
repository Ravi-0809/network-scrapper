from flask import Flask, request, jsonify
from validations import validate_input_data
from job_handler import create_jobs

app = Flask(__name__)

@app.route('/')
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
    
    create_jobs(processed_data=processed_data)

    return jsonify({"message": f"Scheduled {len(processed_data)} jobs successfully"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
