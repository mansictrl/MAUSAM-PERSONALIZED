from services.weather_service import get_weather


weather = get_weather(
    18.5204,
    73.8567
)


print(weather)