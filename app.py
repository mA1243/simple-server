from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

CORS(app)

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_location(city):
    """Fetch latitude and longitude for a given city."""
    try:
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}")
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError("City not found")
        location = {
            "lat": data[0]["lat"],
            "lon": data[0]["lon"]
        }
        return location
    except requests.RequestException as e:
        raise ValueError("Failed to fetch location data")
        

def get_weather_data(lat, lon, unit):
    """Fetch weather data for given coordinates."""
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise ValueError("Failed to fetch weather data")

@app.route('/')
def hello_world():
    """Default route with API information."""
    return jsonify({"message": "Welcome to the Weather API. Use /api/v1/weather to fetch weather data."})

@app.route("/api/v1/weather", methods=["GET"])
def get_weather():
    """Fetch weather data for a given city."""
    try:
        city = request.args.get("city")
        unit = request.args.get("unit", default="metric")
        if not city:
            return jsonify({"error": "City parameter is required"}), 400
        
        location = get_location(city)
        lat = location["lat"]
        lon = location["lon"]
        
        weather_data = get_weather_data(lat, lon, unit)
        temp_data = weather_data["main"]
        current_temp = temp_data["temp"]
        feels_like = temp_data["feels_like"]
        min_temp = temp_data["temp_min"]
        max_temp = temp_data["temp_max"]
        country_data = weather_data["sys"]["country"]
        city_data = weather_data["name"]
        
        weather_icon_data = weather_data["weather"][0]["icon"]
        weather_icon = f"https://openweathermap.org/img/wn/{weather_icon_data}@2x.png"
        
        current_weather = {
            "temperature": {
                "current_temp": current_temp,
                "feels_like": feels_like,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "icon": weather_icon,
                "unit": unit,
                "city": city_data,
                "country": country_data
            }
        }
        return jsonify(current_weather)
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch weather data"}), 500
    except ValueError:
        return jsonify({"error": "City Not Found"})
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors (Not Found)."""
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
