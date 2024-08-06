import time
import requests
import json
import os
from datetime import datetime, timedelta
from data_cache import load_cache, save_cache
from config import WEATHER_CACHE_FILE, TOPO_CACHE_FILE
from weather_data_service import fetch_weather_data
from topography_data_service import fetch_topography_data


# Function to fetch weather data with caching
def fetch_weather_data_with_cache(lat, lon):
    cache = load_cache(WEATHER_CACHE_FILE)
    key = f"{lat},{lon}"
    now = datetime.utcnow()

    if key in cache and now - datetime.fromisoformat(cache[key]['timestamp']) < timedelta(minutes=15):
        print(f"Using cached weather data for {lat}, {lon}")
        return cache[key]['data']
    else:
        weather_data = fetch_weather_data({"latitude": lat, "longitude": lon})
        if weather_data:
            cache[key] = {
                'timestamp': now.isoformat(),
                'data': weather_data
            }
            save_cache(WEATHER_CACHE_FILE, cache)
        return weather_data

# Function to fetch topography data with caching
def fetch_topography_data_with_cache(lat, lon):
    cache = load_cache(TOPO_CACHE_FILE)
    key = f"{lat},{lon}"

    if key in cache:
        print(f"Using cached topography data for {lat}, {lon}")
        return cache[key]
    else:
        topo_data = fetch_topography_data({"latitude": lat, "longitude": lon})
        time.sleep(1)  # Verzögerung von 1 Sekunde zwischen den Anfragen
        if topo_data:
            cache[key] = topo_data
            save_cache(TOPO_CACHE_FILE, cache)
        return topo_data

__all__ = ['fetch_weather_data_with_cache', 'fetch_topography_data_with_cache']


import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def fetch_weather_data(lat, lon):
    # Hier Beispiel-Implementierung mit Dummy-Daten
    return {
        "latitude": lat,
        "longitude": lon,
        "temperature": 20.5,
        "precipitation": 0.1,
        "cloud_coverage": 80,
        "wind_speed": 5.5,
        "pressure": 1015
    }

@app.route('/weather', methods=['GET'])
def get_weather():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    data = fetch_weather_data(lat, lon)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
