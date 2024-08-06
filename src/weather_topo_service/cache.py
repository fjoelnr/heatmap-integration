import json
import os

def load_cache(filename):
    """
    Load cache from a JSON file.
    Parameters:
    - filename (str): The name of the cache file.
    
    Returns:
    dict: The cached data.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def save_cache(filename, data):
    """
    Save cache to a JSON file.
    Parameters:
    - filename (str): The name of the cache file.
    - data (dict): The data to be cached.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
