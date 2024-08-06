import requests
from datetime import datetime
from credentials import OWM_API_KEY
from cache import load_cache, save_cache

def kelvin_to_celsius(kelvin):
    """
    Convert temperature from Kelvin to Celsius.
    """
    return kelvin - 273.15

def convert_temperatures(data):
    """
    Convert all temperature fields in the weather data from Kelvin to Celsius.
    """
    if 'main' in data:
        if 'temp' in data['main']:
            data['main']['temp'] = kelvin_to_celsius(data['main']['temp'])
        if 'feels_like' in data['main']:
            data['main']['feels_like'] = kelvin_to_celsius(data['main']['feels_like'])
        if 'temp_min' in data['main']:
            data['main']['temp_min'] = kelvin_to_celsius(data['main']['temp_min'])
        if 'temp_max' in data['main']:
            data['main']['temp_max'] = kelvin_to_celsius(data['main']['temp_max'])
    return data

def fetch_weather_data(lat, lon):
    """
    Fetch weather data from OpenWeatherMap API.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    
    Returns:
    dict: Weather data for the location.
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        if response.content:  # Ensure the response is not empty
            data = response.json()
            data = convert_temperatures(data)
            return data
        else:
            raise Exception("Received empty response from weather data API")
    except requests.RequestException as e:
        raise Exception(f"Error fetching weather data: {str(e)}")
    except ValueError as e:
        raise Exception(f"Error parsing weather data response: {str(e)}, Response content: {response.content}")

def update_weather_data(lat, lon):
    """
    Update weather data for a specific location and save it to the cache.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    
    Returns:
    dict: Updated weather data for the location.
    """
    cache = load_cache('data_cache/combined_cache.json')
    key = f"{lat},{lon}"
    now = datetime.utcnow().isoformat()
    
    weather_data = fetch_weather_data(lat, lon)
    if key not in cache:
        cache[key] = {}
    cache[key]['weather'] = {
        'timestamp': now,
        'data': weather_data
    }
    save_cache('data_cache/combined_cache.json', cache)
    return weather_data

def get_weather_data(lat, lon):
    """
    Get weather data for a specific location from the cache or update it if not present.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    
    Returns:
    dict: Weather data for the location.
    """
    cache = load_cache('data_cache/combined_cache.json')
    key = f"{lat},{lon}"
    if key in cache and 'weather' in cache[key]:
        return cache[key]['weather']['data']
    else:
        return update_weather_data(lat, lon)
