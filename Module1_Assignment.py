import requests

def get_coordinates(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results")
        if results:
            location = results[0]
            latitude = location.get("latitude")
            longitude = location.get("longitude")
            print(f"\nLocation: {location['name']}, {location.get('country')}")
            print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")
            return latitude, longitude
        else:
            print("No location found.")
    else:
        print("Geocoding API error.")
    return None, None

def get_weather(latitude, longitude):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        current = data.get("current_weather", {})
        temperature = current.get("temperature")
        windspeed = current.get("windspeed")
        weather_code = current.get("weathercode")
        print(f"\nCurrent Weather:")
        print(f"Temperature: {temperature}°C")
        print(f"Wind Speed: {windspeed} km/h")
        print(f"Weather Code: {weather_code}")
    else:
        print("Weather API error.")

def get_weather_by_city(city_name):
    lat, lon = get_coordinates(city_name)
    if lat is not None and lon is not None:
        get_weather(lat, lon)

# ---- Main Execution ----
if __name__ == "__main__":
    city_input = input("Enter a city name (e.g., Dhaka, New York, Delhi): ")
    get_weather_by_city(city_input.strip())
