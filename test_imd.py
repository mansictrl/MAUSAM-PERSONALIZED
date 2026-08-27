import os
from services.imd_api import get_current_weather
from services.weather_service import get_weather
print("--- IMD API Connectivity Test ---")
api_key = os.getenv("IMD_API_KEY")
if not api_key:
    print("Notice: IMD_API_KEY environment variable is not set.")
    print("If IMD provided an API key, set it using: $env:IMD_API_KEY='your_key'\n")

data = get_current_weather()

if data is not None:
    print("Successfully fetched live IMD weather data:")
    print(data)
else:
    print("Could not fetch IMD weather data (HTTP 401 Unauthorized or network issue).")
    print("App will automatically fall back to local data/weather.json.")
