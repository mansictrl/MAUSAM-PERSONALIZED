import os
import requests

IMD_BASE_URL = "https://api.imd.gov.in/api/v1"


def get_headers():
    """
    Construct request headers including optional API key / Authorization token.
    Set environment variable IMD_API_KEY or IMD_AUTH_HEADER if required by IMD.
    """
    headers = {
        "User-Agent": "Mausam-Personalized-App/1.0",
        "Accept": "application/json"
    }

    api_key = os.getenv("IMD_API_KEY")
    auth_header = os.getenv("IMD_AUTH_HEADER")

    if api_key:
        headers["x-api-key"] = api_key
    if auth_header:
        headers["Authorization"] = auth_header

    return headers


def get_current_weather(station_id=None):
    """
    Fetch current weather from IMD API (Endpoint #3 in IMD API Reference).
    """
    url = f"{IMD_BASE_URL}/current_wx"
    params = {}
    if station_id:
        params["id"] = station_id

    try:
        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("IMD current weather error:", error)
        return None


def get_city_forecast(station_id=None):
    """
    Fetch 7-day city forecast from IMD API (Endpoint #1 in IMD API Reference).
    """
    url = f"{IMD_BASE_URL}/cityforecast"
    params = {}
    if station_id:
        params["id"] = station_id

    try:
        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("IMD forecast error:", error)
        return None


def get_city_forecast_mapping():
    """
    Fetch city forecast mapping data (station IDs and names).
    """
    url = f"{IMD_BASE_URL}/cityforecast_mapping"
    try:
        response = requests.get(
            url,
            headers=get_headers(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("IMD city forecast mapping error:", error)
        return None


def get_mausamgram(latitude, longitude):
    """
    Fetch weather at location (Mausamgram - Endpoint #6 in IMD API Reference).
    """
    url = f"{IMD_BASE_URL}/mausamgram"
    params = {
        "lat": latitude,
        "lon": longitude
    }
    try:
        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("IMD Mausamgram error:", error)
        return None


def get_sunmoon(latitude, longitude):
    """
    Fetch sunrise, sunset, moonrise, and moonset for user coordinates (Endpoint #23 in IMD API Reference).
    """
    url = f"{IMD_BASE_URL}/sunmoon"
    params = {
        "lat": latitude,
        "lon": longitude
    }
    try:
        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("IMD Sun/Moon error:", error)
        return None