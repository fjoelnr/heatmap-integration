import numpy as np

def process_data(weather_data, topography_data):
    """
    Processes the weather and topography data into a format suitable for output.
    
    Parameters:
        weather_data (list): The weather data.
        topography_data (list): The topography data.
        
    Returns:
        dict: The processed data.
    """
    lat_grid = np.array([d['latitude'] for d in weather_data]).reshape(-1, 1)
    lon_grid = np.array([d['longitude'] for d in weather_data]).reshape(-1, 1)

    processed_data = {
        "latitude": lat_grid.flatten().tolist(),
        "longitude": lon_grid.flatten().tolist(),
        "temperature": [d['temperature'] for d in weather_data],
        "precipitation": [d['precipitation'] for d in weather_data],
        "cloud_coverage": [d['cloud_coverage'] for d in weather_data],
        "wind_speed": [d['wind_speed'] for d in weather_data],
        "pressure": [d['pressure'] for d in weather_data],
        "topography": [d['topography'] for d in topography_data]
    }
    
    return processed_data

# Export the function
__all__ = ['process_data']
