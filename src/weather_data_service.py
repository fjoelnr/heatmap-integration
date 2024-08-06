# weather_data_service.py

import requests
import json
import jsonschema
from jsonschema import validate

from credentials import OWM_API_KEY
from config import requ_schema, resp_schema


def fetch_weather_data(area):
    # Validierung der Anfragedaten
    if not validate_json(area, requ_schema):
        return {"error": "Ungültige Anfragedaten"}
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    lat = area['latitude']
    lon = area['longitude']
    api_key = OWM_API_KEY

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "latitude": lat,
            "longitude": lon,
            "temperature": data["main"]["temp"],
            "precipitation": data.get("rain", {}).get("1h", 0),
            "cloud_coverage": data["clouds"]["all"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"]
        }
        return weather_data
    else:
        print(f"Fehler bei der Wetterdaten-Abfrage: {response.status_code}, {response.text}")
        return None

def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print("JSON-Daten sind ungültig:", err)
        return False
    return True

if __name__ == "__main__":
    # Beispiel-Anfragedaten
    area = {
        "latitude": 48.1662,
        "longitude": 11.2222
    }

    weather_data = fetch_weather_data(area)
    print(json.dumps(weather_data, indent=4))
