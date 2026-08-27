from datetime import datetime


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def calculate_fitness_score(weather):
    temperature = weather["temperature"]
    humidity = weather["humidity"]
    wind = weather["wind_speed"]
    rain = weather["rain_probability"]

    score = 100

    # Temperature
    if temperature > 35:
        score -= 25
    elif temperature > 32:
        score -= 15
    elif temperature > 30:
        score -= 8

    # Humidity
    if humidity > 85:
        score -= 20
    elif humidity > 75:
        score -= 12
    elif humidity > 65:
        score -= 5

    # Wind
    if wind > 30:
        score -= 15
    elif wind > 20:
        score -= 8

    # Rain
    if rain > 70:
        score -= 30
    elif rain > 50:
        score -= 20
    elif rain > 30:
        score -= 10

    return clamp(score)


def calculate_health_score(weather):
    temperature = weather["temperature"]
    humidity = weather["humidity"]
    uv = weather["uv_index"]

    score = 100

    # Heat
    if temperature > 38:
        score -= 30
    elif temperature > 34:
        score -= 20
    elif temperature > 31:
        score -= 10

    # Humidity
    if humidity > 85:
        score -= 20
    elif humidity > 75:
        score -= 12
    elif humidity > 65:
        score -= 5

    # UV
    if uv >= 11:
        score -= 30
    elif uv >= 8:
        score -= 20
    elif uv >= 6:
        score -= 12
    elif uv >= 3:
        score -= 5

    return clamp(score)


def calculate_travel_score(weather):
    temperature = weather["temperature"]
    rain = weather["rain_probability"]
    wind = weather["wind_speed"]

    score = 100

    if rain > 80:
        score -= 35
    elif rain > 60:
        score -= 25
    elif rain > 40:
        score -= 15
    elif rain > 20:
        score -= 5

    if wind > 40:
        score -= 25
    elif wind > 30:
        score -= 15
    elif wind > 20:
        score -= 5

    if temperature > 40:
        score -= 20
    elif temperature > 35:
        score -= 10

    return clamp(score)


def calculate_commute_score(weather):
    rain = weather["rain_probability"]
    wind = weather["wind_speed"]

    score = 100

    if rain > 80:
        score -= 40
    elif rain > 60:
        score -= 30
    elif rain > 40:
        score -= 18
    elif rain > 20:
        score -= 8

    if wind > 40:
        score -= 25
    elif wind > 30:
        score -= 15
    elif wind > 20:
        score -= 5

    return clamp(score)


def find_best_fitness_time(forecast):
    best_slot = None
    best_score = -1

    for slot in forecast:
        score = 100

        temperature = slot["temperature"]
        rain = slot["rain_probability"]

        # Temperature
        if temperature > 35:
            score -= 30
        elif temperature > 32:
            score -= 15
        elif temperature > 30:
            score -= 5

        # Rain
        if rain > 70:
            score -= 40
        elif rain > 50:
            score -= 25
        elif rain > 30:
            score -= 10

        if score > best_score:
            best_score = score
            best_slot = slot

    if best_slot:
        time_value = best_slot["time"]

        try:
            return datetime.fromisoformat(
                time_value
            ).strftime("%I:%M %p").lstrip("0")
        except (ValueError, TypeError):
            return time_value

    return "No suitable time"


def fitness_result(weather, forecast):
    score = calculate_fitness_score(weather)

    if score >= 80:
        title = "Excellent conditions for a run"
    elif score >= 60:
        title = "Good conditions with some precautions"
    elif score >= 40:
        title = "Exercise with caution"
    else:
        title = "Poor conditions for outdoor activity"

    return {
        "score": score,
        "title": title,
        "best_time": find_best_fitness_time(forecast),
        "icon": "🏃",
        "cards": [
            {
                "icon": "✓",
                "type": "green",
                "title": "Fitness conditions",
                "text": title
            },
            {
                "icon": "!",
                "type": "orange",
                "title": "Humidity",
                "text": (
                    f"Current humidity is "
                    f"{weather['humidity']}%. "
                    "Stay hydrated during outdoor activity."
                )
            },
            {
                "icon": "☁",
                "type": "blue",
                "title": "Rain probability",
                "text": (
                    f"Current rain probability is "
                    f"{weather['rain_probability']}%."
                )
            }
        ]
    }


def health_result(weather):
    score = calculate_health_score(weather)

    if score >= 80:
        title = "Comfortable health conditions"
    elif score >= 60:
        title = "Moderate health conditions"
    elif score >= 40:
        title = "Take precautions outdoors"
    else:
        title = "Poor conditions for prolonged exposure"

    uv = weather["uv_index"]
    humidity = weather["humidity"]

    return {
        "score": score,
        "title": title,
        "best_time": "Before 10:00 AM",
        "icon": "♥",
        "cards": [
            {
                "icon": "!",
                "type": "orange",
                "title": "Humidity",
                "text": (
                    f"Humidity is currently {humidity}%. "
                    "High humidity may increase discomfort."
                )
            },
            {
                "icon": "☀",
                "type": "orange",
                "title": "UV protection",
                "text": (
                    f"UV Index is {uv}. "
                    "Consider appropriate sun protection."
                )
            },
            {
                "icon": "✓",
                "type": "green",
                "title": "Recommended time",
                "text": (
                    "Morning conditions are generally more "
                    "comfortable for outdoor activity."
                )
            }
        ]
    }


def travel_result(weather):
    score = calculate_travel_score(weather)

    if score >= 80:
        title = "Mostly favorable travel conditions"
    elif score >= 60:
        title = "Travel with some precautions"
    elif score >= 40:
        title = "Check conditions before travelling"
    else:
        title = "Unfavorable travel conditions"

    return {
        "score": score,
        "title": title,
        "best_time": "2:00 – 5:00 PM",
        "icon": "✈",
        "cards": [
            {
                "icon": "✓",
                "type": "green",
                "title": "Travel conditions",
                "text": title
            },
            {
                "icon": "!",
                "type": "orange",
                "title": "Weather alert",
                "text": (
                    f"Rain probability is currently "
                    f"{weather['rain_probability']}%."
                )
            },
            {
                "icon": "☂",
                "type": "blue",
                "title": "Packing suggestion",
                "text": (
                    "Keep an umbrella or rain protection "
                    "available if travelling later."
                )
            }
        ]
    }


def commute_result(weather):
    score = calculate_commute_score(weather)

    if score >= 80:
        title = "Good conditions for commuting"
    elif score >= 60:
        title = "Mostly manageable commute"
    elif score >= 40:
        title = "Plan your commute carefully"
    else:
        title = "Potentially difficult commute"

    return {
        "score": score,
        "title": title,
        "best_time": "Before 5:00 PM",
        "icon": "🚗",
        "cards": [
            {
                "icon": "!",
                "type": "orange",
                "title": "Commute conditions",
                "text": title
            },
            {
                "icon": "✓",
                "type": "green",
                "title": "Better travel window",
                "text": (
                    "Earlier travel may help avoid worsening "
                    "weather conditions."
                )
            },
            {
                "icon": "→",
                "type": "blue",
                "title": "Plan ahead",
                "text": (
                    f"Rain probability is currently "
                    f"{weather['rain_probability']}%."
                )
            }
        ]
    }


# =========================
# BEACH & WATER
# =========================

def calculate_beach_score(weather):
    temperature = weather["temperature"]
    rain = weather["rain_probability"]
    wind = weather["wind_speed"]

    score = 100

    if temperature < 20:
        score -= 20
    elif temperature < 24:
        score -= 10

    if rain > 80:
        score -= 35
    elif rain > 60:
        score -= 25
    elif rain > 40:
        score -= 15

    if wind > 40:
        score -= 25
    elif wind > 30:
        score -= 15
    elif wind > 20:
        score -= 5

    return clamp(score)


def beach_result(weather):
    score = calculate_beach_score(weather)

    if score >= 80:
        title = "Excellent conditions for outdoor water activities"
    elif score >= 60:
        title = "Mostly favorable beach conditions"
    elif score >= 40:
        title = "Check conditions before heading out"
    else:
        title = "Unfavorable beach conditions"

    return {
        "score": score,
        "title": title,
        "best_time": "Morning",
        "icon": "🏖️",
        "cards": [
            {
                "icon": "✓",
                "type": "green",
                "title": "Beach conditions",
                "text": title
            },
            {
                "icon": "☀",
                "type": "orange",
                "title": "Temperature",
                "text": (
                    f"Current temperature is "
                    f"{weather['temperature']}°."
                )
            },
            {
                "icon": "🌧",
                "type": "blue",
                "title": "Rain probability",
                "text": (
                    f"Current rain probability is "
                    f"{weather['rain_probability']}%."
                )
            }
        ]
    }


# =========================
# FAMILY & SCHOOL
# =========================

def calculate_family_score(weather):
    rain = weather["rain_probability"]
    wind = weather["wind_speed"]
    temperature = weather["temperature"]

    score = 100

    if rain > 80:
        score -= 35
    elif rain > 60:
        score -= 25
    elif rain > 40:
        score -= 15

    if wind > 40:
        score -= 25
    elif wind > 30:
        score -= 15
    elif wind > 20:
        score -= 5

    if temperature > 40:
        score -= 20
    elif temperature > 35:
        score -= 10

    return clamp(score)


def family_result(weather):
    score = calculate_family_score(weather)

    if score >= 80:
        title = "Good conditions for family activities"
    elif score >= 60:
        title = "Mostly manageable conditions"
    elif score >= 40:
        title = "Plan school and outdoor activities carefully"
    else:
        title = "Difficult conditions for outdoor activities"

    return {
        "score": score,
        "title": title,
        "best_time": "Morning",
        "icon": "👨‍👩‍👧",
        "cards": [
            {
                "icon": "✓",
                "type": "green",
                "title": "Family conditions",
                "text": title
            },
            {
                "icon": "🌧",
                "type": "blue",
                "title": "Rain alert",
                "text": (
                    f"Rain probability is currently "
                    f"{weather['rain_probability']}%."
                )
            },
            {
                "icon": "→",
                "type": "orange",
                "title": "Plan ahead",
                "text": (
                    "Check weather conditions before school "
                    "or outdoor travel."
                )
            }
        ]
    }


# =========================
# AGRICULTURE & GARDENING
# =========================

def calculate_agriculture_score(weather):
    rain = weather["rain_probability"]
    temperature = weather["temperature"]
    wind = weather["wind_speed"]

    score = 100

    # Extreme heat
    if temperature > 40:
        score -= 30
    elif temperature > 35:
        score -= 15

    # Very heavy rain probability
    if rain > 80:
        score -= 25
    elif rain > 60:
        score -= 15

    # Strong wind
    if wind > 40:
        score -= 25
    elif wind > 30:
        score -= 15

    return clamp(score)


def agriculture_result(weather):
    score = calculate_agriculture_score(weather)

    if score >= 80:
        title = "Favorable conditions for gardening"
    elif score >= 60:
        title = "Generally suitable conditions"
    elif score >= 40:
        title = "Monitor weather before outdoor work"
    else:
        title = "Weather may affect agricultural activities"

    return {
        "score": score,
        "title": title,
        "best_time": "Early morning",
        "icon": "🌱",
        "cards": [
            {
                "icon": "🌱",
                "type": "green",
                "title": "Growing conditions",
                "text": title
            },
            {
                "icon": "🌧",
                "type": "blue",
                "title": "Rain probability",
                "text": (
                    f"Rain probability is currently "
                    f"{weather['rain_probability']}%."
                )
            },
            {
                "icon": "🌡",
                "type": "orange",
                "title": "Temperature",
                "text": (
                    f"Current temperature is "
                    f"{weather['temperature']}°."
                )
            }
        ]
    }


# =========================
# OUTDOOR EVENTS
# =========================

def calculate_event_score(weather):
    temperature = weather["temperature"]
    rain = weather["rain_probability"]
    wind = weather["wind_speed"]

    score = 100

    if rain > 80:
        score -= 40
    elif rain > 60:
        score -= 30
    elif rain > 40:
        score -= 20
    elif rain > 20:
        score -= 10

    if wind > 40:
        score -= 25
    elif wind > 30:
        score -= 15
    elif wind > 20:
        score -= 5

    if temperature > 40:
        score -= 25
    elif temperature > 35:
        score -= 15
    elif temperature < 15:
        score -= 15

    return clamp(score)


def events_result(weather):
    score = calculate_event_score(weather)

    if score >= 80:
        title = "Excellent conditions for an outdoor event"
    elif score >= 60:
        title = "Good conditions with some planning"
    elif score >= 40:
        title = "Consider a backup plan"
    else:
        title = "Outdoor event conditions may be challenging"

    return {
        "score": score,
        "title": title,
        "best_time": "Late afternoon",
        "icon": "💍",
        "cards": [
            {
                "icon": "✓",
                "type": "green",
                "title": "Event conditions",
                "text": title
            },
            {
                "icon": "🌧",
                "type": "orange",
                "title": "Rain probability",
                "text": (
                    f"Rain probability is "
                    f"{weather['rain_probability']}%."
                )
            },
            {
                "icon": "💨",
                "type": "blue",
                "title": "Wind",
                "text": (
                    f"Current wind speed is "
                    f"{weather['wind_speed']} km/h."
                )
            }
        ]
    }


# =========================
# GENERATE PERSONALIZATION
# =========================

def generate_personalization(weather, forecast):
    return {
        "fitness": fitness_result(
            weather,
            forecast
        ),

        "health": health_result(
            weather
        ),

        "travel": travel_result(
            weather
        ),

        "commute": commute_result(
            weather
        ),

        "beach": beach_result(
            weather
        ),

        "family": family_result(
            weather
        ),

        "agriculture": agriculture_result(
            weather
        ),

        "events": events_result(
            weather
        )
    }