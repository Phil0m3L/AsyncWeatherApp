# Asynchronous Weather App

## About

This is an web application which uses the [WeatherAPI.com](https://www.weatherapi.com/) API to fetch weather data for a given location. The application is built using the `Quart` web framework and uses the `aiohttp` library to make HTTP requests to the [WeatherAPI.com](https://www.weatherapi.com/) API.

## Prerequisites

- Git
- Python 3.8 or higher (tested on 3.11)
- [WeatherAPI.com](https://www.weatherapi.com/) API key

## Installation

```shell
# Clone the repository
git clone https://github.com/Rhythm273/AsyncWeatherApp.git
# Switch to the project directory
cd AsyncWeatherApp
# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
# Install the dependencies
pip install -r requirements.txt
```

## Configuration

Copy the `config.example.py` file to `config.py` and update the `SECRET_KEY` variable with a 32-bit hexadecimal string and the `WEATHER_API_KEY` variable with your [WeatherAPI.com](https://www.weatherapi.com/) API key.

## Running

### Development

```shell
python launcher.py
```

### Production

```shell
hypercorn launcher:app
```

## License

[GNU General Public License v3.0](LICENSE)

Copyright &copy; 2024 Manomita Debnath
