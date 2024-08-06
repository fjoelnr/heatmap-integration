import json
import os

# Load cache from a file
def load_cache(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

# Save cache to a file
def save_cache(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

__all__ = ['load_cache', 'save_cache']
