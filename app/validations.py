from flask import jsonify
from marshmallow import ValidationError
from representations import URLInput

input_schema = URLInput()

def validate_input_data(data):
    # Ensure the input is a list of JSON objects
    if not isinstance(data, list):
        raise Exception("list of JSON objects is required")
    
    if (len(data) == 0):
        raise Exception("empty input found")
    
    # Process each JSON object in the list with schema validation
    processed_data = []
    for item in data:
        try:
            validated_data = input_schema.load(item)
            processed_data.append(validated_data)
        except ValidationError as err:
            raise Exception(err.messages)
    
    return processed_data