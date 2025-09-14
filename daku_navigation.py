import os
import requests
from livekit.agents import function_tool
from dotenv import load_dotenv

# ================================
# 🔹 FIXED COORDINATES (আপনার location এখানে বসান)
# ================================
MY_LAT = 23.749095     # Example: Dhaka
MY_LON = 90.382116     # Example: Dhaka
# ================================
load_dotenv(".env.local")
# Load Google Maps API Key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


@function_tool()
async def navigate_to(destination: str) -> str:
    """
    Navigates from fixed current location to a destination using Google Maps Directions API.

    Example usage:
    - "Take me to Farmgate"
    - "Navigate to Motijheel"
    """

    if not GOOGLE_MAPS_API_KEY:
        return "Boss, Google Maps API Key missing. Please set GOOGLE_MAPS_API_KEY in your .env file."

    # Origin is fixed coordinates
    origin = f"{MY_LAT},{MY_LON}"
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",  # can also use 'walking', 'transit'
        "language": "bn",   # Bangla response
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") != "OK":
            return f"Boss, navigation failed: {data.get('status')}"

        route = data["routes"][0]["legs"][0]
        distance = route["distance"]["text"]
        duration = route["duration"]["text"]

        steps = []
        for step in route["steps"]:
            # Remove HTML tags
            instruction = step["html_instructions"]
            clean_instruction = (
                instruction.replace("<b>", "")
                           .replace("</b>", "")
                           .replace("<div style=\"font-size:0.9em\">", " ")
                           .replace("</div>", "")
            )
            steps.append(clean_instruction)

        result = f"Boss, আমি route পেয়ে গেছি {destination}-এর জন্য।\n"
        result += f"মোট দূরত্ব: {distance}, আনুমানিক সময় লাগবে: {duration}.\n\n"
        result += "প্রথম কয়েকটা নির্দেশনা:\n" + "\n".join([f"- {s}" for s in steps[:5]])  

        return result

    except Exception as e:
        return f"Error while fetching navigation: {e}"
