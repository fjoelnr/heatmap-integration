from flask import Flask, request, jsonify
from input_service.data_fetch import fetch_weather_data, fetch_topography_data
from input_service.validate_json import validate_json

app = Flask(__name__)

@app.route('/fetch_weather', methods=['GET'])
def fetch_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if lat and lon:
        data = fetch_weather_data(float(lat), float(lon))
        return jsonify(data)
    else:
        return jsonify({"error": "Missing latitude or longitude"}), 400

@app.route('/fetch_topography', methods=['GET'])
def fetch_topography():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if lat and lon:
        data = fetch_topography_data(float(lat), float(lon))
        return jsonify(data)
    else:
        return jsonify({"error": "Missing latitude or longitude"}), 400

@app.route('/validate', methods=['POST'])
def validate():
    json_data = request.json
    schema_path = request.args.get('schema', '/schemas/in_schema.json')
    valid = validate_json(json_data, schema_path)
    return jsonify({"valid": valid})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
