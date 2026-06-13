import requests
import urllib.parse

def get_coordinates(address):
    headers = {
        'User-Agent': 'TravelCalculatorBot/1.0'
    }
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&limit=1"

    response = requests.get(url, headers=headers)
    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return float(data['lon']), float(data['lat'])
    else:
        print(f"Error finding coordinates for: {address}")
        return None


def get_route_details(start_coords, end_coords):
    # OSRM expects coordinates in the format: longitude,latitude
    coords_string = f"{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
    url = f"http://router.project-osrm.org/route/v1/driving/{coords_string}?overview=false"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 'Ok':
            # TODO
            distance_miles = 0
            distance_km = 0
            duration_mins = 0
            fuel_used_liters = 0 # compute using travel speed of 50 km/h

            return {
                "distance_miles": round(distance_miles, 2),
                "distance_km": round(distance_km, 2),
                "duration_minutes": round(duration_mins, 1),
                "fuel_liters": round(fuel_used_liters, 2)
            }

    print("Error calculating route.")
    return None


# --- Main Execution ---
if __name__ == "__main__":
    # Define your addresses
    start_address = "Camara Municipal do Porto, Porto , Portugal" # TODO
    end_address = "Ponte Arrabida, Porto Portugal" # TODO

    start_coords = get_coordinates(start_address)
    end_coords = get_coordinates(end_address)

    if start_coords and end_coords:
        result = get_route_details(start_coords, end_coords)

        if result:
            print(f"Route: From '{start_address}' to '{end_address}'")
            print("-" * 50)
            print(f"Distance:       {result['distance_miles']} miles ({result['distance_km']} km)")
            print(f"Travel Time:    {result['duration_minutes']} minutes")
            print(f"Estimated Fuel: {result['fuel_liters']} gallons (assumption of 50 Km/h)")