# app/utils/geo.py
import math
from typing import Optional


def haversine_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Compute great-circle distance between two points (in km).
    """
    R = 6371.0  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def compute_speed_kmph(
    distance_km: float,
    hours: float
) -> Optional[float]:
    if hours <= 0:
        return None
    return distance_km / hours
