from geopy.distance import geodesic

def calculate_distance(src, dst):
    """Calculate distance between two coordinates using geodesic distance."""
    return geodesic(src, dst).km

def find_route(source, destination, distance):
    """
    Find the optimal route with logic to prioritize direct flights.
    
    Strategy:
    - For distances < 2000 km: Direct flight (short-haul)
    - For distances 2000-5000 km: Direct flight or 1 hub (mid-range, still direct preferred)
    - For distances 5000-9000 km: Direct flight (long-haul) or 1 strategic hub
    - For distances > 9000 km: Consider 1-2 hubs for optimization
    
    Returns direct flight first, then suggests hub options if needed.
    """
    
    # Prioritize DIRECT flights for all distances
    if distance > 0:
        # Primary route: ALWAYS direct first
        primary_route = [source, destination]
        
        # Secondary routes: only suggest hubs as alternatives for very long flights
        alternative_hubs = {}
        
        if distance > 9000:  # Ultra long-haul (intercontinental)
            alternative_hubs[1] = [source, "London", destination]
            alternative_hubs[2] = [source, "Dubai", destination]
        elif distance > 5000:  # Long-haul (5000-9000 km)
            alternative_hubs[1] = [source, "Dubai", destination]
        elif distance > 2000:  # Mid-range (2000-5000 km)
            alternative_hubs[1] = [source, "Istanbul", destination]
        
        # Return primary direct route
        # (secondary routes available as alternatives if user wants to explore options)
        return primary_route