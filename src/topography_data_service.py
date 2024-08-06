# topography_data_service.py

import requests
import json
import jsonschema
from jsonschema import validate

from credentials import OPENTOPO_API_KEY
from config import requ_schema, resp_schema


def fetch_topography_data(area):
    # Validierung der Anfragedaten
    if not validate_json(area, requ_schema):
        return {"error": "Ungültige Anfragedaten"}

    lat = area["latitude"]
    lon = area["longitude"]
    url = f"https://api.opentopodata.org/v1/eudem25m?locations={lat},{lon}"
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        data = response.json()
        elevation = data["results"][0]["elevation"]
        return {
            "latitude": lat,
            "longitude": lon,
            "topography": elevation
        }
    else:
        print(f"Fehler bei der Topografiedaten-Abfrage: {response.status_code}, {response.text}")
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

    topography_data = fetch_topography_data(area)
    print(json.dumps(topography_data, indent=4))
