"""
Tools for the ReAct agent.

This file defines individual tools. Import them in agent.py and add to the tools list there.
"""

import random
from datetime import datetime
from zoneinfo import ZoneInfo
from langchain.tools import Tool

from utils import make_request


def calculator(expression: str) -> str:
    print("\n🔢 Calculator tool running...\n")
    try:
        # Evaluate the expression
        result = eval(expression)
        return f"The result of {expression} is {result}\n"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}\n"


def random_int(range_str: str = "1-100") -> str:
    print("\n🎲 Random int tool running...\n")
    try:
        # Support both "1-10" and "1,10" formats
        if '-' in range_str:
            min_val, max_val = range_str.split('-')
        elif ',' in range_str:
            min_val, max_val = range_str.split(',')
        else:
            return "Error: Please use format like '1-10' or '1,100'\n"
        
        min_val = int(min_val.strip())
        max_val = int(max_val.strip())
        
        result = random.randint(min_val, max_val)
        return f"Random integer between {min_val} and {max_val}: {result}\n"
    except Exception as e:
        return f"Error generating random integer: {str(e)}\n"


def geocode(city_name: str) -> str:
    """Look up latitude/longitude for a city."""
    print(f"\n🌍 Geocode tool running...\n")
    print(f"[TOOL] Executing geocode with parameters: city_name='{city_name}'")
    
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    success, data = make_request(url)
    
    if not success:
        return f"Error: {data}\n"
    
    if "results" in data and len(data["results"]) > 0:
        result = data["results"][0]
        return f"City: {result['name']}, {result.get('country', '')}\nLatitude: {result['latitude']}\nLongitude: {result['longitude']}\nTimezone: {result.get('timezone', '')}\n"
    else:
        return f"Error: City '{city_name}' not found\n"


def weather(coordinates: str) -> str:
    """Get weather information from weather.gov API.
    
    Args:
        coordinates: String in format "latitude, longitude"
    
    Example API call:
    curl -L -H "User-Agent: ReActAgent/1.0" "https://api.weather.gov/points/47.6062,-122.3321"
        Given properties->forecast, curl that URL for the forecast data
    """
    print(f"\n🌤️  Weather tool running...\n")
    print(f"[TOOL] Executing weather with parameters: coordinates='{coordinates}'")
    
    # Parse the coordinates string
    parts = coordinates.split(',')
    try:
        latitude = float(parts[0].strip())
        longitude = float(parts[1].strip())
    except (ValueError, IndexError):
        return "Error: Invalid latitude/longitude values\n"
    
    # Step 1: Get the forecast URL from the points endpoint
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {"User-Agent": "ReActAgent/1.0"}
    success, data = make_request(url, headers=headers)
    
    if not success:
        return f"Error: {data}\n"
    
    # Step 2: Get the forecast from the forecast URL
    forecast_url = data["properties"]["forecast"]
    success, forecast_data = make_request(forecast_url, headers=headers)
    
    if not success:
        return f"Error: {forecast_data}\n"
    
    # Get first period (current/upcoming)
    if forecast_data["properties"]["periods"]:
        period = forecast_data["properties"]["periods"][0]
        return f"{period['name']}: {period['temperature']}°{period['temperatureUnit']}\n{period['shortForecast']}\n{period['detailedForecast']}\n"
    
    return "Error: No forecast data available\n"


def time(timezone: str) -> str:
    """Get current time for a timezone.
    
    Note: This is computed locally using Python's datetime and zoneinfo,
    not via an external API call.
    """
    print(f"\n🕐 Time tool running...\n")
    print(f"[TOOL] Executing time with parameters: timezone='{timezone}'")
    try:
        tz = ZoneInfo(timezone)
        current_time = datetime.now(tz)
        return f"Timezone: {timezone}\nTime: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\nFormatted: {current_time.strftime('%I:%M %p')}\n"
    except Exception as e:
        return f"Error: {str(e)}\n"


# Tool definitions - all Tool() instances are defined at the bottom
calculator_tool = Tool(
    name="calculator",
    func=calculator,
    description="Performs basic arithmetic calculations. Input should be a mathematical expression as a string (e.g., '2 + 2', '10 * 5', '100 / 4'). Use this tool when you need to perform mathematical calculations.",
)

random_int_tool = Tool(
    name="random_int",
    func=random_int,
    description="Generates a random integer within a specified range. Input should be a range like '1-10' or '1,100' for min and max values. If no input is provided, defaults to 1-100. Use this tool when you need to generate a random integer.",
)

geocode_tool = Tool(
    name="geocode",
    func=geocode,
    description="Looks up latitude and longitude coordinates for a city name. Input should be a city name as a string (e.g., 'Seattle', 'New York', 'Tokyo'). Returns the city's coordinates, country, and timezone. Use this tool when you need to find the geographic coordinates of a city.",
)

weather_tool = Tool(
    name="weather",
    func=weather,
    description="Gets current weather information from weather.gov API. Input should be coordinates in the format 'latitude, longitude' (e.g., '47.6062, -122.3321'). Returns temperature, forecast, and detailed weather information. Use this tool when you need weather information for specific coordinates.",
)

time_tool = Tool(
    name="time",
    func=time,
    description="Gets the current time for a specific timezone. Input should be a timezone name (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo'). Returns the current time in that timezone in multiple formats. Use this tool when you need to know what time it is in a specific location.",
)
