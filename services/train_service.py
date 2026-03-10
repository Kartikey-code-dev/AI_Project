import math


def get_train_info(source_city: str, destination_city: str, distance_km: float, travelers: int = 1):
    """
    Lightweight train estimate (no external API dependency).
    Returns an estimated fare range and duration range.
    """
    distance_km = max(0.0, float(distance_km or 0.0))
    travelers = max(1, int(travelers or 1))

    # Typical India intercity averages; kept conservative.
    avg_speed_kmph = 65.0
    duration_hours = distance_km / avg_speed_kmph if avg_speed_kmph else 0.0
    min_h = max(1.0, duration_hours * 0.85)
    max_h = max(min_h, duration_hours * 1.35)

    # Very rough fare estimate per person per km; scaled with distance.
    # Short distances skew higher per-km due to minimum ticketing.
    per_km_low = 0.90 if distance_km >= 300 else 1.10
    per_km_high = 1.80 if distance_km >= 300 else 2.20
    base_min = 120.0  # minimum ticket ballpark
    base_max = 250.0

    per_person_low = base_min + (distance_km * per_km_low)
    per_person_high = base_max + (distance_km * per_km_high)
    total_low = per_person_low * travelers
    total_high = per_person_high * travelers

    def fmt_rupees(v: float) -> str:
        return f"₹{int(math.ceil(v)):,}"

    def fmt_hours(h: float) -> str:
        hh = int(h)
        mm = int(round((h - hh) * 60))
        if mm == 60:
            hh += 1
            mm = 0
        return f"{hh}h {mm:02d}m"

    return {
        "price": f"{fmt_rupees(total_low)} - {fmt_rupees(total_high)} ({travelers} traveler{'s' if travelers != 1 else ''})",
        "duration_range": f"{fmt_hours(min_h)} - {fmt_hours(max_h)}",
        "recommended_class": "Sleeper / 3A (budget) or 2A (comfort)",
        "source": source_city,
        "destination": destination_city,
        "note": "For live trains, check IRCTC / RailYatri / Google Transit (availability varies by date).",
    }
