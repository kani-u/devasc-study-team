import os
import requests

API_KEY = os.getenv("GRAPHHOPPER_API_KEY")

def geocode(place):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": place,
        "limit": 1,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200 or not data.get("hits"):
        print(f"Location not found: {place}")
        return None

    point = data["hits"][0]["point"]
    return point["lat"], point["lng"]


def main():
    if not API_KEY:
        print("API key not configured.")
        return

    start = input("Starting location: ")
    destination = input("Destination: ")

    print("\nTransport: car, bike, foot")
    vehicle = input("Choose transport: ").lower()

    if vehicle not in ["car", "bike", "foot"]:
        print("Invalid transport mode.")
        return

    start_point = geocode(start)
    end_point = geocode(destination)

    if not start_point or not end_point:
        return

    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [
            f"{start_point[0]},{start_point[1]}",
            f"{end_point[0]},{end_point[1]}"
        ],
        "vehicle": vehicle,
        "key": API_KEY,
        "instructions": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        print("Routing error:", data.get("message", response.status_code))
        return

    path = data["paths"][0]

    print("\n--- ROUTE INFORMATION ---")
    print(f"Distance: {path['distance'] / 1000:.2f} km")
    print(f"Time: {path['time'] / 60000:.1f} minutes")

    print("\n--- DIRECTIONS ---")
    for instruction in path["instructions"]:
        print(f"- {instruction['text']} ({instruction['distance']:.0f} m)")


if __name__ == "__main__":
    main()
