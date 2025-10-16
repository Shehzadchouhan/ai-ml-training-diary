import os
import requests
import logging
from dotenv import load_dotenv
from langchain.tools import tool

# Load .env variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_city():
    """Automatically detect user's city based on IP."""
    try:
        response = requests.get("https://ipinfo.io", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("city", "Unknown")
        else:
            logger.error(f"❌ IP detection failed: {response.status_code}")
            return "Unknown"
    except Exception as e:
        logger.error(f"❌ IP detection error: {e}")
        return "Unknown"


@tool
def get_weather(city: str = "") -> str:
    """
    Gives current weather information for a given city.

    Use this tool when the user asks about weather, rain, temperature, humidity, or wind.
    If no city is given, detect city automatically.

    Example prompts:
    - "आज का मौसम कैसा है?"
    - "Weather बताओ Bangalore का"
    - "क्या बारिश होगी मुंबई में?"
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        logger.error("❌ OpenWeather API key missing.")
        return "Environment variables में OpenWeather API key नहीं मिली।"

    # Auto-detect city if not provided
    if not city:
        city = get_current_city()
        if city == "Unknown":
            return "❌ City detect नहीं हो पाया। कृपया manually city बताएं।"

    logger.info(f"🌤 Fetching weather for city: {city}")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        if response.status_code != 200:
            logger.error(f"❌ API Error: {response.status_code} - {response.text}")
            return f"⚠️ {city} के लिए weather fetch नहीं कर पाए। कृपया city name चेक करें।"

        data = response.json()
        weather = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        result = (
            f"🌤 **Weather in {city}:**\n"
            f"• Condition: {weather}\n"
            f"• Temperature: {temperature}°C\n"
            f"• Humidity: {humidity}%\n"
            f"• Wind Speed: {wind_speed} m/s"
        )

        logger.info(f"✅ Weather fetched successfully for {city}")
        return result

    except Exception as e:
        logger.exception(f"❌ Weather fetch exception: {e}")
        return "⚠️ Weather fetch करते समय एक error आया।"
