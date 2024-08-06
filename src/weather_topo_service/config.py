import os

# Interval for periodic data fetching in seconds
FETCH_INTERVAL = int(os.getenv('FETCH_INTERVAL', 300))

# Cache-Datei
WEATHER_CACHE_FILE = 'data_cache/weather_cache.json'
