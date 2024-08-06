import requests
from datetime import datetime
from credentials import TOPO_API_KEY
from cache import load_cache, save_cache

def fetch_topography_data(lat, lon):
    """
    Fetch topography data from an external API.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    
    Returns:
    dict: Topography data for the location.
    """
    try:
        url = f"https://api.opentopodata.org/v1/eudem25m?locations={lat},{lon}&apikey={TOPO_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        if response.content:  # Ensure the response is not empty
            return response.json()
        else:
            raise Exception("Received empty response from topography data API")
    except requests.RequestException as e:
        raise Exception(f"Error fetching topography data: {str(e)}")
    except ValueError as e:
        raise Exception(f"Error parsing topography data response: {str(e)}, Response content: {response.content}")

def update_topography_data(lat, lon):
    """
    Update topography data for a specific location and save it to the cache.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    
    Returns:
    dict: Updated topography data for the location.
    """
    cache = load_cache('data_cache/combined_cache.json')
    key = f"{lat},{lon}"
    now = datetime.utcnow().isoformat()
    
    topo_data = fetch_topography_data(lat, lon)
    if key not in cache:
        cache[key] = {}
    cache[key]['topography'] = {
        'timestamp': now,
        'data': topo_data
    }
    save_cache('data_cache/combined_cache.json', cache)
    return topo_data

def get_topography_data(lat, lon):
    """
    Get topography data for a specific location from the cache or update it if not present.
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    
    Returns:
    dict: Topography data for the location.
    """
    cache = load_cache('data_cache/combined_cache.json')
    key = f"{lat},{lon}"
    if key in cache and 'topography' in cache[key]:
        return cache[key]['topography']['data']
    else:
        return update_topography_data(lat, lon)
