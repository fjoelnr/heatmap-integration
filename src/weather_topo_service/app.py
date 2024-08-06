from flask import Flask, request, jsonify
from redis import Redis, RedisError
from scheduler import start_scheduler
from weather_data_service import get_weather_data
from topography_data_service import get_topography_data


app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/weather', methods=['GET'])
def weather():
    """
    Endpoint to get weather data for a specific location.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    - field (str, optional): Specific field of weather data to retrieve (e.g., 'temp').
    
    Returns:
    JSON response containing weather data or specific field of weather data.
    """
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    field = request.args.get('field')
    if lat and lon:
        try:
            data = get_weather_data(float(lat), float(lon))
            if field:
                if field in data['main']:
                    return jsonify({field: data['main'][field]})
                else:
                    return jsonify({"error": f"Field '{field}' not found in weather data"}), 400
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Missing latitude or longitude"}), 400

@app.route('/topo', methods=['GET'])
def topography():
    """
    Endpoint to get topography data for a specific location.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    - field (str, optional): Specific field of topography data to retrieve (e.g., 'elevation').
    
    Returns:
    JSON response containing topography data or specific field of topography data.
    """
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    field = request.args.get('field')
    if lat and lon:
        try:
            data = get_topography_data(float(lat), float(lon))
            if field:
                # Handle different structures in topography data
                if field == 'elevation':
                    results = data.get('results', [])
                    if results and 'elevation' in results[0]:
                        return jsonify({field: results[0]['elevation']})
                elif field in data:
                    return jsonify({field: data[field]})
                else:
                    return jsonify({"error": f"Field '{field}' not found in topography data"}), 400
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Missing latitude or longitude"}), 400

@app.route('/')
def hello():
    try:
        redis.incr('hits')
        counter = str(redis.get('hits'), 'utf-8')
    except RedisError as e:
        return f"Error connecting to Redis: {e}", 500
    return f"Hi! This Webpage has been viewed {counter} times"

@app.route('/info')
def info():
    resp = {
        'connecting_ip': request.headers.get('X-Real-IP', request.remote_addr),
        'proxy_ip': request.headers.get('X-Forwarded-For', request.remote_addr),
        'host': request.headers.get('Host'),
        'user-agent': request.headers.get('User-Agent')
    }
    return jsonify(resp)

@app.route('/flask-health-check')
def flask_health_check():
    return "success"

if __name__ == '__main__':
    start_scheduler()
    app.run(host='0.0.0.0', port=8000)
