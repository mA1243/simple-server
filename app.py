from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

CORS(app)

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_location(city):
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}")
    response.raise_for_status()
    data = response.json()
    location = {
        "lat": data[0]["lat"],
        "lon" : data[0]["lon"]
    }
    return location

def get_weather_data(lat, lon):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    response.raise_for_status()
    data = response.json()
    return data

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/getWeather")
def get_weather():
    try:
        city = request.args.get("city")
        location = get_location(city)
        lat = location["lat"]
        lon = location["lon"]
        weather_data = get_weather_data(lat, lon)
        temp = weather_data["main"]["temp"]
        unit = "celsius"
        current_weather = {
            "temperature": {
                "value": temp,
                "unit": unit
            }
        }
        return jsonify(current_weather)
    except:
        return "City Not Found"

if __name__ == "__main__":
    app.run(debug=True)
