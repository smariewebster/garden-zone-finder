import pgeocode
import requests

# USDA Growing zones based on average annual minimum temperature
# Source: USDA Plant Hardiness Zone Map
ZONE_FROST_DATES = {
    "5a": {"last_spring_frost": "May 15", "first_fall_frost": "Oct 1"},
    "5b": {"last_spring_frost": "May 10", "first_fall_frost": "Oct 8"},
    "6a": {"last_spring_frost": "Apr 25", "first_fall_frost": "Oct 15"},
    "6b": {"last_spring_frost": "Apr 15", "first_fall_frost": "Oct 22"},
    "7a": {"last_spring_frost": "Apr 5",  "first_fall_frost": "Nov 1"},
    "7b": {"last_spring_frost": "Mar 25", "first_fall_frost": "Nov 10"},
    "8a": {"last_spring_frost": "Mar 15", "first_fall_frost": "Nov 15"},
    "8b": {"last_spring_frost": "Mar 1",  "first_fall_frost": "Nov 20"},
    "9a": {"last_spring_frost": "Feb 15", "first_fall_frost": "Dec 1"},
    "9b": {"last_spring_frost": "Feb 1",  "first_fall_frost": "Dec 15"},
}

def get_location_info(zipcode):
    """Takes a zip code and returns city, state, lat, longitude."""
    nomi = pgeocode.Nominatim('us')
    result = nomi.query_postal_code(zipcode)

    if result is None or result.empty or str(result.place_name) == 'nan':
        return None

    return {
        "city": result.place_name,
        "state": result.state_name,
        "lat": result.latitude,
        "lng": result.longitude,
    }

def get_growing_zone(zipcode):
    """Uses zip code to look up USDA growing zone via the Phzmapi API."""
    try:
        url = f"https://phzmapi.org/{zipcode}.json"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get("zone", "Unknown")
    except Exception as e:
        print(f"Could not fetch growing zone: {e}")
        return "Unknown"

def get_frost_dates(zone):
    """Returns frost dates for a given zone. Falls back gracefully."""
    zone_lower = zone.lower()
    return ZONE_FROST_DATES.get(zone_lower, {
        "last_spring_frost": "Check local extension office",
        "first_fall_frost": "Check local extension office"
    })

def lookup(zipcode):
    """Main function - takes zip code, returns all location + zone data."""
    location = get_location_info(zipcode)

    if not location:
        print(f"Could not find location for zip code: {zipcode}")
        return None

    zone = get_growing_zone(zipcode)
    frost = get_frost_dates(zone)

    return {
        "zipcode": zipcode,
        "city": location["city"],
        "state": location["state"],
        "zone": zone,
        "last_spring_frost": frost["last_spring_frost"],
        "first_fall_frost": frost["first_fall_frost"],
    }
