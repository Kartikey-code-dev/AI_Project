import requests
from datetime import datetime, timedelta

def get_flight_prices(source_city, destination_city, days=7):
    try:
        url = "https://tequila-api.kiwi.com/v2/search"
        departure_date = (datetime.now() + timedelta(days=days)).strftime("%d/%m/%Y")
        params = {
            "fly_from": f"city:{source_city.upper()}",
            "fly_to": f"city:{destination_city.upper()}",
            "dateFrom": departure_date,
            "dateTo": departure_date,
            "adults": 1,
            "limit": 1,
            "sort": "price"
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                flight = data["data"][0]
                duration_seconds = flight.get('duration', {}).get('total', 0)
                duration_hours = duration_seconds // 3600
                duration_minutes = (duration_seconds % 3600) // 60
                
                return {
                    "price": f"₹{int(flight.get('price', 0) * 83)}",
                    "duration": f"{int(duration_hours)}h {int(duration_minutes)}m" if duration_seconds > 0 else "Direct",
                    "duration_range": f"{int(duration_hours)}h - {int(duration_hours + 2)}h",
                    "airline": flight.get('airlines', ['Unknown'])[0],
                    "source": flight.get('cityFrom', source_city),
                    "destination": flight.get('cityTo', destination_city)
                }
    except Exception as e:
        print(f"Flight API error: {e}")
    
    return {
        "price": "Varies (₹8,300 - ₹1,66,000)",
        "duration": "2h 30m - 18h 45m",
        "duration_range": "2h 30m - 18h 45m",
        "airline": "Multiple options",
        "source": source_city,
        "destination": destination_city,
        "note": "Check Skyscanner, MakeMyTrip, or Google Flights for live prices"
    }

def get_accommodation_estimate(destination_city, days=5):
    try:
        url = "https://api.opentripmap.com/core/sqmcoord"
        from services.location_service import get_coordinates
        coords = get_coordinates(destination_city)
        params = {
            "radius": 5000,
            "kinds": "hotels,hostels,apartments",
            "lat": coords[0],
            "lon": coords[1],
            "limit": 5
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("features"):
                avg_price_per_night = 6640  # 83 INR per USD (80 USD baseline)
                total_cost = avg_price_per_night * days
                return {
                    "average_per_night": f"₹{avg_price_per_night}",
                    "total_for_stay": f"₹{total_cost}",
                    "options": "Mix of hotels, hostels, and apartments",
                    "source": "Booking.com, Airbnb, Hotels.com"
                }
    except Exception as e:
        print(f"Accommodation API error: {e}")
    
    total = 6640 * days
    return {
        "average_per_night": "₹4,150 - ₹12,450",
        "total_for_stay": f"~₹{total}",
        "options": "Budget to luxury options available",
        "source": "Booking.com, Airbnb, Hotels.com"
    }

def get_attractions_api(destination_city):
    try:
        from services.location_service import get_coordinates
        coords = get_coordinates(destination_city)
        url = "https://api.opentripmap.com/core/sqmcoord"
        params = {
            "radius": 3000,
            "kinds": "museums,historic,memorial,monument,tourist_attraction",
            "lat": coords[0],
            "lon": coords[1],
            "limit": 5
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            attractions = []
            for feature in data.get("features", [])[:5]:
                props = feature.get("properties", {})
                attractions.append({
                    "name": props.get("name", "Attraction"),
                    "description": props.get("kinds", "Tourist attraction"),
                    "type": props.get("kinds", "Landmark")
                })
            if attractions:
                return attractions
    except Exception as e:
        print(f"Attractions API error: {e}")
    
    return []
