# Weather Service

The Weather Service fetches and serves weather data for specific locations using the OpenWeatherMap API. It includes functionality for periodic data updates and caching.

## Features

- Fetch weather data for specific coordinates.
- Periodic updates for cached locations.
- REST API to get weather data.

## Requirements

- Docker
- Docker Compose

## Setup

- Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-directory>

- Create a .env file with the following content:
    ```env
    OWM_API_KEY=your_openweathermap_api_key
    FETCH_INTERVAL=600

- Build and run the Docker containers:
    ```sh
    docker-compose up --build

## Usage
Fetch Weather Data

- To fetch weather data for specific coordinates, use the following endpoint:

    ```http
    GET /weather?lat=<latitude>&lon=<longitude>

- Example:

    ```bash
    http://localhost:8000/weather?lat=48.1265&lon=11.0276

- Project Structure

    ```markdown
    /src/weather_service
    ├── __init__.py
    ├── app.py
    ├── cache.py
    ├── config.py
    ├── credentials.py
    ├── scheduler.py
    ├── weather_data_service.py
    ├── requirements.txt
    ├── Dockerfile
    ├── compose.yaml
    └── data_cache
        ├── geo_cache.json
        └── weather_cache.json

## Testing

- To run the tests, use the following command:

    ```sh
    pytest tests/