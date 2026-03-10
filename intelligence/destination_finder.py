import requests
from services.flight_service import get_attractions_api

# Curated database of major attractions by city
ATTRACTIONS_DB = {
    "london": [
        {"name": "Big Ben & Houses of Parliament", "description": "Iconic Gothic Revival architecture and seat of UK Parliament. Stunning views from Westminster Bridge.", "type": "Historical"},
        {"name": "Tower of London", "description": "Historic castle housing the Crown Jewels. Medieval fortress with 1000 years of history.", "type": "Historical"},
        {"name": "Buckingham Palace", "description": "Official London residence of the monarch. One of the most recognizable buildings in the world.", "type": "Royal"},
        {"name": "Tower Bridge", "description": "Victorian Gothic Revival bascule and suspension bridge. Stunning architecture over the Thames.", "type": "Landmark"},
        {"name": "British Museum", "description": "World's largest museum with over 8 million artifacts. Free entry to main galleries.", "type": "Museum"},
    ],
    "new york": [
        {"name": "Statue of Liberty", "description": "Iconic copper statue symbolizing freedom. UNESCO World Heritage site on Liberty Island.", "type": "Landmark"},
        {"name": "Times Square", "description": "Bustling commercial intersection in Midtown Manhattan. Known for bright LED advertisements and theaters.", "type": "Entertainment"},
        {"name": "Central Park", "description": "Urban park spanning 843 acres. Perfect for walks, picnics, and outdoor activities.", "type": "Nature"},
        {"name": "Empire State Building", "description": "Art Deco skyscraper with observation decks. 360-degree views of NYC from 86th floor.", "type": "Landmark"},
        {"name": "Metropolitan Museum of Art", "description": "World-renowned art museum. Houses over 2 million works of art spanning 5000 years.", "type": "Museum"},
    ],
    "paris": [
        {"name": "Eiffel Tower", "description": "Iron lattice tower and symbol of Paris. Built in 1889, stands 330m tall with stunning city views.", "type": "Landmark"},
        {"name": "Louvre Museum", "description": "World's largest art museum and home to the Mona Lisa. Historic palace converted to museum.", "type": "Museum"},
        {"name": "Arc de Triomphe", "description": "Massive stone arch honoring those who died in wars. Champs-Élysées views from the top.", "type": "Historical"},
        {"name": "Notre-Dame Cathedral", "description": "Medieval Catholic cathedral. Masterpiece of French Gothic architecture along the Seine.", "type": "Religious"},
        {"name": "Versailles Palace", "description": "Stunning royal residence with elaborate gardens. Symbol of French royal power and art.", "type": "Royal"},
    ],
    "dubai": [
        {"name": "Burj Khalifa", "description": "World's tallest building at 828m. Observation decks offer breathtaking city and desert views.", "type": "Landmark"},
        {"name": "Palm Jumeirah", "description": "Artificial palm-shaped island. Luxury homes and resorts overlooking the Arabian Gulf.", "type": "Nature"},
        {"name": "Dubai Mall", "description": "World's largest shopping mall with 1200+ stores. Home to aquarium and entertainment zones.", "type": "Shopping"},
        {"name": "Gold Souk", "description": "Traditional Arab marketplace selling gold jewelry. Experience authentic Dubai culture.", "type": "Cultural"},
        {"name": "Desert Safari", "description": "Thrilling dune bashing followed by bedouin camp. Camel rides and traditional entertainment.", "type": "Adventure"},
    ],
    "tokyo": [
        {"name": "Senso-ji Temple", "description": "Ancient Buddhist temple in Asakusa. Tokyo's oldest temple with stunning red lantern.", "type": "Religious"},
        {"name": "Tokyo Tower", "description": "Red lattice communications tower. 360-degree views of Tokyo from observation decks.", "type": "Landmark"},
        {"name": "Meiji Shrine", "description": "Shinto shrine dedicated to Emperor Meiji. Located in peaceful forested area of Shibuya.", "type": "Religious"},
        {"name": "Shibuya Crossing", "description": "World's busiest pedestrian crossing. Iconic intersection witnessed by millions of visitors.", "type": "Cultural"},
        {"name": "teamLab Borderless", "description": "Digital art museum with immersive installations. Cutting-edge technology meets contemporary art.", "type": "Museum"},
    ],
    "singapore": [
        {"name": "Marina Bay Sands", "description": "Iconic hotel with rooftop Infinity Pool. Stunning views of Singapore harbor.", "type": "Landmark"},
        {"name": "Gardens by the Bay", "description": "Futuristic gardens with Supertrees and climate-controlled domes. Beautiful LED light shows.", "type": "Nature"},
        {"name": "Sentosa Island", "description": "Island resort with beaches, attractions, and theme parks. Universal Studios Singapore located here.", "type": "Beach"},
        {"name": "Chinatown Heritage Centre", "description": "Museum showcasing Chinese immigrant history. Original shop-houses and artifacts.", "type": "Cultural"},
        {"name": "Merlion Park", "description": "Iconic half-lion, half-fish statue. Singapore's national symbol since 1972.", "type": "Landmark"},
    ],
    "chennai": [
        {"name": "Kapaleeshwarar Temple", "description": "Ancient Hindu temple with stunning Dravidian architecture. Built in 7th century, dedicated to Lord Shiva.", "type": "Religious"},
        {"name": "Marina Beach", "description": "One of India's longest beaches. 13km stretch of sand along the Bay of Bengal.", "type": "Beach"},
        {"name": "Government Museum", "description": "Repository of art, artifacts, and antiquities. Bronze sculptures and ancient manuscripts.", "type": "Museum"},
        {"name": "Parthasarathy Temple", "description": "Ancient Dravidian temple with intricate carvings. Dedicated to Lord Krishna.", "type": "Religious"},
        {"name": "San Thome Basilica", "description": "Historic Roman Catholic church built over St. Thomas's tomb. Gothic-Romanesque architecture.", "type": "Religious"},
    ],
    "default": [
        {"name": "Main City Center", "description": "Vibrant downtown area with shops, restaurants, and local culture.", "type": "Cultural"},
        {"name": "Local Museum", "description": "Museum showcasing regional history and artifacts.", "type": "Museum"},
        {"name": "Heritage Sites", "description": "Historic landmarks reflecting the city's rich cultural heritage.", "type": "Historical"},
        {"name": "Public Gardens", "description": "Beautiful urban park perfect for leisurely strolls.", "type": "Nature"},
        {"name": "Local Markets", "description": "Experience authentic local shopping and traditional crafts.", "type": "Shopping"},
    ]
}

def get_places(city):
    """Get curated attractions for a city.
    
    Args:
        city (str): city name
    Returns:
        list: list of attraction dictionaries with name, description, and type
    """
    city_lower = city.lower().strip()
    
    # Try real API first (OpenTripMap)
    try:
        api_attractions = get_attractions_api(city)
        if api_attractions:
            return api_attractions
    except:
        pass
    
    # Try direct match in curated database
    if city_lower in ATTRACTIONS_DB:
        return ATTRACTIONS_DB[city_lower]
    
    # Try partial match
    for key in ATTRACTIONS_DB:
        if key in city_lower or city_lower in key:
            return ATTRACTIONS_DB[key]
    
    # Fallback: try to fetch from Wikipedia/OSM
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"tourist attractions {city}",
            "format": "json",
            "limit": 5
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        attractions = []
        for item in data[:5]:
            attractions.append({
                "name": item.get("display_name", "Attraction").split(",")[0],
                "description": f"Popular attraction in {city}. {item.get('type', 'Must-visit')}",
                "type": item.get('type', 'Landmark')
            })
        
        if attractions:
            return attractions
    except:
        pass
    
    # Return default attractions
    return ATTRACTIONS_DB["default"]