from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session
)

import json
import os

from services.personalization import generate_personalization
from services.weather_service import get_weather

import firebase_admin
from firebase_admin import credentials, firestore, auth


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "mausam-development-secret-key"
)

# =========================
# FIREBASE ADMIN
# =========================

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth


# =========================
# FIREBASE ADMIN
# =========================

firebase_credentials = os.environ.get(
    "FIREBASE_ADMIN_CREDENTIALS"
)

if firebase_credentials:

    cred = credentials.Certificate(
        json.loads(firebase_credentials)
    )

else:

    cred = credentials.Certificate(
        "firebase-admin-key.json"
    )


if not firebase_admin._apps:

    firebase_admin.initialize_app(cred)


firestore_db = firestore.client()


# =========================
# FALLBACK WEATHER DATA
# =========================

def load_fallback_weather():

    data_path = os.path.join(
        "data",
        "weather.json"
    )

    with open(
        data_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =========================
# START / ONBOARDING
# =========================

@app.route("/")
def start():

    return redirect(
        url_for("login")
    )


@app.route("/signup")
def signup():

    return render_template(
        "signup.html"
    )


@app.route("/preferences")
def preferences():

    return render_template(
        "preferences.html"
    )


@app.route("/location")
def location():

    return render_template(
        "location.html"
    )


@app.route("/login")
def login():

    return render_template(
        "login.html"
    )


# =========================
# FIREBASE LOGIN
# =========================

@app.route(
    "/auth/login",
    methods=["POST"]
)
def authenticate_login():

    data = request.get_json()

    if not data:

        return {
            "success": False,
            "error": "No login data received"
        }, 400


    id_token = data.get(
        "idToken"
    )


    if not id_token:

        return {
            "success": False,
            "error": "Missing authentication token"
        }, 400


    try:

        decoded_token = (
            auth.verify_id_token(
                id_token
            )
        )


        uid = decoded_token["uid"]


        # Store authenticated UID
        # in Flask session

        session["uid"] = uid


        print(
            "Authenticated user:",
            uid
        )


        return {
            "success": True
        }


    except Exception as error:

        print(
            "Authentication error:",
            error
        )


        return {
            "success": False,
            "error": "Invalid authentication token"
        }, 401


# =========================
# PERSONALIZED HOMEPAGE
# =========================

@app.route("/home")
def personalized_home():

    # =========================
    # GET LOGGED-IN USER
    # =========================

    uid = session.get(
        "uid"
    )


    if not uid:

        return redirect(
            url_for("login")
        )


    print(
        "Session UID:",
        uid
    )


    # =========================
    # GET USER FROM FIRESTORE
    # =========================

    user_ref = (
        firestore_db
        .collection("users")
        .document(uid)
    )


    user_doc = user_ref.get()


    if not user_doc.exists:

        print(
            "User document not found:",
            uid
        )

        return redirect(
            url_for("signup")
        )


    user_data = (
        user_doc.to_dict()
    )


    print(
        "Logged-in user data:",
        user_data
    )


    # =========================
    # USER INFORMATION
    # =========================

    user_name = user_data.get(
        "name",
        "User"
    )


    interests = user_data.get(
        "interests",
        []
    )


    location_data = user_data.get(
        "location"
    )


    # =========================
    # USER LOCATION
    # =========================

    if location_data:

        latitude = location_data.get(
            "latitude"
        )

        longitude = location_data.get(
            "longitude"
        )

    else:

        latitude = None
        longitude = None


    # =========================
    # FALLBACK LOCATION
    # =========================

    if latitude is None:

        latitude = 18.5204


    if longitude is None:

        longitude = 73.8567


    print(
        "Weather coordinates:",
        latitude,
        longitude
    )


    # =========================
    # OPEN-METEO
    # =========================

    weather_data = get_weather(
        latitude,
        longitude
    )


    # =========================
    # FALLBACK WEATHER
    # =========================

    if weather_data is None:

        print(
            "Open-Meteo unavailable. "
            "Using fallback weather data."
        )

        weather = (
            load_fallback_weather()
        )

    else:

        weather = weather_data


    # =========================
    # PERSONALIZATION
    # =========================

    current_weather = weather[
        "current"
    ]


    personalization_weather = {

        "temperature":
            current_weather[
                "temperature"
            ],

        "humidity":
            current_weather[
                "humidity"
            ],

        "wind_speed":
            current_weather[
                "wind_speed"
            ],

        "rain_probability":
            current_weather[
                "rain_probability"
            ],

        "uv_index":
            current_weather[
                "uv_index"
            ]

    }


    personalized_data = (
        generate_personalization(
            personalization_weather,
            weather["forecast"]
        )
    )


    # =========================
    # RENDER HOMEPAGE
    # =========================

    return render_template(

        "index.html",

        weather=weather,

        personalized_data=
            personalized_data,

        user_name=
            user_name,

        user_interests=
            interests,

        user_location=
            location_data

    )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )