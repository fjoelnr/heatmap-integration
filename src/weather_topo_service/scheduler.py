import time
from threading import Thread
from config import FETCH_INTERVAL
from weather_data_service import update_weather_data
from topography_data_service import update_topography_data
from cache import load_cache

def scheduled_fetch():
    """
    Function to periodically update weather and topography data for all cached locations.
    This function runs in a separate thread.
    """
    while True:
        cache = load_cache('data_cache/combined_cache.json')
        for key in cache.keys():
            lat, lon = map(float, key.split(','))
            update_weather_data(lat, lon)
            update_topography_data(lat, lon)
        time.sleep(FETCH_INTERVAL)

def start_scheduler():
    """
    Function to start the scheduler in a daemon thread.
    """
    thread = Thread(target=scheduled_fetch)
    thread.daemon = True
    thread.start()
