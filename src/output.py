import folium
from folium.plugins import HeatMap
import json
import numpy as np

def create_map_output(data):
    if not data:
        raise ValueError("Data for map output is empty")

    center = [data[0]['latitude'], data[0]['longitude']]
    map_ = folium.Map(location=center, zoom_start=6)

    for entry in data:
        folium.Marker(
            location=[entry['latitude'], entry['longitude']],
            popup=json.dumps(entry, indent=4)
        ).add_to(map_)

    output_path = 'data/map.html'
    map_.save(output_path)
    return {"map_path": output_path}

def prepare_heatmap_data(latitudes, longitudes, values):
    return [[lat, lon, value] for lat, lon, value in zip(latitudes, longitudes, values)]

def create_heatmap(center, heatmap_data, gradients):
    m = folium.Map(location=center, zoom_start=6)
    
    for key, data in heatmap_data.items():
        HeatMap(data, name=key, min_opacity=0.2, max_zoom=18, gradient=gradients.get(key, {})).add_to(m)
    
    folium.LayerControl().add_to(m)
    return m

def create_heatmap_output(data):
    if not data:
        raise ValueError("Data for heatmap output is empty")
    
    center = [data[0]['latitude'], data[0]['longitude']]
    latitudes = [entry['latitude'] for entry in data]
    longitudes = [entry['longitude'] for entry in data]

    heatmap_data = {
        "Temperature": prepare_heatmap_data(
            latitudes,
            longitudes,
            [entry['temperature'] for entry in data]
        ),
        "Precipitation": prepare_heatmap_data(
            latitudes,
            longitudes,
            [entry['precipitation'] for entry in data]
        ),
        "Cloud Coverage": prepare_heatmap_data(
            latitudes,
            longitudes,
            [entry['cloud_coverage'] for entry in data]
        ),
        "Wind Speed": prepare_heatmap_data(
            latitudes,
            longitudes,
            [entry['wind_speed'] for entry in data]
        ),
        "Pressure": prepare_heatmap_data(
            latitudes,
            longitudes,
            [entry['pressure'] for entry in data]
        ),
        "Topography": prepare_heatmap_data(
            latitudes,
            longitudes,
            [entry['topography'] for entry in data]
        )
    }

    gradients = {
        "Temperature": {0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 1: 'red'},
        "Precipitation": {0.2: 'purple', 0.4: 'blue', 0.6: 'cyan', 1: 'white'},
        "Cloud Coverage": {0.2: 'black', 0.5: 'gray', 0.8: 'white'},
        "Wind Speed": {0.2: 'green', 0.4: 'yellow', 0.6: 'orange', 1: 'red'},
        "Pressure": {0.2: 'blue', 0.4: 'lightblue', 0.6: 'green', 1: 'yellow'},
        "Topography": {0.0: 'black', 0.5: 'gray', 1.0: 'white'}
    }

    heatmap = create_heatmap(center, heatmap_data, gradients)

    output_path = 'data/heatmap.html'
    heatmap.save(output_path)
    
    return {"heatmap_path": output_path}

def generate_output(processed_data):
    if not processed_data['data']:
        raise ValueError("Processed data is empty")
    
    map_output = create_map_output(processed_data['data'])
    heatmap_output = create_heatmap_output(processed_data['data'])
    return {**map_output, **heatmap_output}

# Export the function
__all__ = ['generate_output']
