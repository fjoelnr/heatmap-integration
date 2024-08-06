import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEATHER_CACHE_FILE = os.path.join(BASE_DIR, 'data_cache', 'weather_cache.json')
TOPO_CACHE_FILE = os.path.join(BASE_DIR, 'data_cache', 'topography_cache.json')
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'in.json')

# Load schemas

with open(os.path.join(BASE_DIR, 'schemas', 'in_schema.json')) as f:
    in_schema = json.load(f)

with open(os.path.join(BASE_DIR, 'schemas', 'out_schema.json')) as f:
    out_schema = json.load(f)


# Lade das JSON-Schema für die Anfragedaten
with open(os.path.join(BASE_DIR, 'schemas', 'requ_schema.json')) as f:
    requ_schema = json.load(f)

# Lade das JSON-Schema für die Antwortdaten
with open(os.path.join(BASE_DIR, 'schemas', 'resp_schema.json')) as f:
    resp_schema = json.load(f)
