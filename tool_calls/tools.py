import requests
from rich import print
from dotenv import load_dotenv
import os

load_dotenv()
WEATHER_API_KEY = os.getenv("WKEY")


def get_weather(city: str):
    parameters = {
        "q": city,
        "key": WEATHER_API_KEY
    }

    response = requests.get(
        url="https://api.weatherapi.com/v1/current.json",
        params=parameters
    )
    data = response.json()
    current = data["current"]
    return {
        "condition": current["condition"]["text"],
        "temp_c": current["temp_c"],
        "is_day": bool(current["is_day"]),
        "wind_kph": current["wind_kph"],
        "pressure_mb": current["pressure_mb"],
        "humidity": current["humidity"],
        "feelslike_c": current["feelslike_c"]
    }


get_weather_definition = {
    "type": "function",
    "function": {
        "name": "weather",
        "description": "Retrieves weather information for desired city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The desired location of weather"},
            },
            "required": ["city"]
        }
    }
}

import requests
from rich import print
from dotenv import load_dotenv
import os
import json # Make sure json is imported if you're using it for debugging prints

load_dotenv()
WEATHER_API_KEY = os.getenv("WKEY")

# (Keep your existing get_weather function and get_weather_definition here)

def forecast(city: str, days: int):
    parameters = {
        "q": city,
        "key": WEATHER_API_KEY,
        "days": days
    }

    response = requests.get(
        url="https://api.weatherapi.com/v1/forecast.json",
        params=parameters
    )

    data = response.json()

    # Extract forecast data for all requested days
    forecast_days_data = []
    if "forecast" in data and "forecastday" in data["forecast"]:
        for day_data in data["forecast"]["forecastday"]:
            # 'day_data' now represents each item in the 'forecastday' list
            # It contains 'date', 'day', 'astro', etc.
            day_summary = day_data["day"] # This is the "day" object for a specific forecast day

            forecast_days_data.append({
                "date": day_data["date"], # Date is directly in day_data
                "condition": day_summary["condition"]["text"],
                "avgtemp_c": day_summary["avgtemp_c"], # Use avgtemp_c for daily average
                "maxtemp_c": day_summary["maxtemp_c"],
                "mintemp_c": day_summary["mintemp_c"],
                "maxwind_kph": day_summary["maxwind_kph"],
                "avghumidity": day_summary["avghumidity"],
                "daily_chance_of_rain": day_summary["daily_chance_of_rain"],
                "daily_chance_of_snow": day_summary["daily_chance_of_snow"]
            })

    return forecast_days_data # Return a list of forecast data for each day


forecast_definition = {
    "type": "function",
    "function": {
        "name": "forecast",
        "description": "Retrieves weather forecast information for a desired city for a number of days.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The desired location for weather forecast"},
                "days": {"type": "integer", "description": "Number of days to forecast, between 1 and 10 (or 14 depending on your WeatherAPI plan)"},
            },
            "required": ["city", "days"]
        }
    }
}