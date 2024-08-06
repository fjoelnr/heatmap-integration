import os
import json
import numpy as np
from data_fetch import fetch_weather_data_with_cache, fetch_topography_data_with_cache
from data_processing import process_data
from output import generate_output
from validate_json import validate_json
from config import in_schema, out_schema, INPUT_FILE

def handle_request(input_data):
    # Validierung der Eingangsdaten
    if not validate_json(input_data, in_schema):
        return {"error": "Ungültige Eingangsdaten"}

    areas = input_data['areas']
    weather_data = []
    topography_data = []

    for area in areas:
        if area['type'] == 'rectangle':
            north = area['boundaries']['north']
            south = area['boundaries']['south']
            east = area['boundaries']['east']
            west = area['boundaries']['west']
            spacing = area['spacing']


            latitudes = np.round(np.arange(south, (north + spacing), spacing), 3)
            longitudes = np.round(np.arange(west, (east + spacing), spacing), 3)
            for lat in latitudes:
                for lon in longitudes:
                    # print(lat, lon)
                    weather = fetch_weather_data_with_cache(lat, lon)
                    if weather:
                        weather_data.append(weather)
                    else:
                        print(f"Fehler beim Abrufen der Wetterdaten für Lat: {lat}, Lon: {lon}")
                    topo = fetch_topography_data_with_cache(lat, lon)
                    if topo:
                        topography_data.append(topo)
                    else:
                        print(f"Fehler beim Abrufen der Topologiedaten für Lat: {lat}, Lon: {lon}")

        elif area['type'] in ['grid', 'circle']:
            latitude = area.get('latitude')
            longitude = area.get('longitude')
            weather = fetch_weather_data_with_cache(latitude, longitude)
            if weather:
                weather_data.append(weather)
            else:
                print(f"Fehler beim Abrufen der Wetterdaten für Lat: {latitude}, Lon: {longitude}")
            topo = fetch_topography_data_with_cache(latitude, longitude)
            if topo:
                topography_data.append(topo)
            else:
                print(f"Fehler beim Abrufen der Topologiedaten für Lat: {latitude}, Lon: {longitude}")

    if not weather_data and not topography_data:
        print("Es wurden keine Wetter- oder Topologiedaten abgerufen.")
        return {"error": "Es wurden keine Wetter- oder Topologiedaten abgerufen."}

    # Kombinieren der Daten in das erforderliche Format
    combined_data = []
    for w, t in zip(weather_data, topography_data):
        combined_entry = {
            "latitude": w["latitude"],
            "longitude": w["longitude"],
            "height_layer": 0,  # Beispielwert, wenn es eine Höhe geben sollte
            "temperature": w["temperature"],
            "precipitation": w["precipitation"],
            "cloud_coverage": w["cloud_coverage"],
            "wind_speed": w["wind_speed"],
            "pressure": w["pressure"],
            "topography": t["topography"]
        }
        combined_data.append(combined_entry)

    processed_data = {"data": combined_data}

    # Validierung der Ausgangsdaten
    if not validate_json(processed_data, out_schema):
        return {"error": "Ungültige Ausgangsdaten"}

    print(f"Processed data: {json.dumps(processed_data, indent=2)}")

    # Ausgabe generieren
    output = generate_output(processed_data)
    return output

if __name__ == "__main__":
    input_file = INPUT_FILE
    with open(input_file, "r") as f:
        input_data = json.load(f)

    result = handle_request(input_data)
    print(f"Result: {result}")

    if "map_path" in result:
        map_path = os.path.join(os.getcwd(), result["map_path"])
        os.system(f"start {map_path}")
    
    if "heatmap_path" in result:
        heatmap_path = os.path.join(os.getcwd(), result["heatmap_path"])
        os.system(f"start {heatmap_path}")
