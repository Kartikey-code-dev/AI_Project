def recommend_places(places):
    """Generate detailed recommendations for places/attractions.
    
    Args:
        places (list): list of attraction dictionaries from get_places()
    Returns:
        list: formatted recommendation strings with descriptions
    """
    recommendations = []
    
    for idx, place in enumerate(places, 1):
        if isinstance(place, dict):
            # Handle dict format with name, description, type
            name = place.get('name', 'Attraction')
            desc = place.get('description', 'Must-visit attraction')
            place_type = place.get('type', 'Landmark')
            recommendation = f"{idx}. {name} ({place_type})\n   {desc}"
        else:
            # Handle string format (fallback)
            recommendation = f"{idx}. {place}\n   A must-visit attraction in your destination."
        
        recommendations.append(recommendation)
    
    return recommendations