import requests
from datetime import datetime

def format_time(value):
    dt = datetime.fromisoformat(value)
    return dt.strftime("%I:%M %p").lstrip("0")

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def weather_code_to_condition(code):

    conditions = {

        0: "Clear sky",

        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Depositing rime fog",

        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",

        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",

        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",

        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",

        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }

    return conditions.get(
        code,
        "Unknown"
    )


def get_weather(
    latitude,
    longitude
):

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "current": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "wind_speed_10m",
            "weather_code",
            "uv_index"
        ]),

        "hourly": ",".join([
            "temperature_2m",
            "precipitation_probability",
            "relative_humidity_2m",
            "wind_speed_10m"
        ]),

        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "sunrise",
            "sunset"
        ]),

        "timezone": "auto",

        "forecast_days": 7
    }


    try:

        response = requests.get(
            OPEN_METEO_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()


        current = data["current"]

        hourly = data["hourly"]

        daily = data["daily"]


        # Current hour's rain probability

        current_hour_index = 0

        rain_probability = (
            hourly["precipitation_probability"]
            [current_hour_index]
        )


        weather = {

            "temperature":
                round(
                    current["temperature_2m"]
                ),

            "feels_like":
                round(
                    current["apparent_temperature"]
                ),

            "humidity":
                current["relative_humidity_2m"],

            "wind_speed":
                round(
                    current["wind_speed_10m"]
                ),

            "uv_index":
                round(
                    current["uv_index"]
                ),

            "rain_probability":
                rain_probability,

            "condition":
                weather_code_to_condition(
                    current["weather_code"]
                ),

            "high":
                round(
                    daily["temperature_2m_max"][0]
                ),

            "low":
                round(
                    daily["temperature_2m_min"][0]
                ),

           "sunrise": format_time(daily["sunrise"][0]),


            "sunset": format_time(daily["sunset"][0])

        }


        # Build forecast for personalization

        forecast = []

        for i in range(
            len(hourly["time"])
        ):

            forecast.append({

                "time":
                    hourly["time"][i],

                "temperature":
                    hourly["temperature_2m"][i],

                "rain_probability":
                    hourly[
                        "precipitation_probability"
                    ][i]

            })


        return {

            "current": weather,

            "forecast": forecast,

            "location": {

                "latitude":
                    data["latitude"],

                "longitude":
                    data["longitude"]

            }

        }


    except requests.RequestException as error:

        print(
            "Open-Meteo error:",
            error
        )

        return None