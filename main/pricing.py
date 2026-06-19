import math


def _haversine_km(lat1, lon1, lat2, lon2):
    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
    except (TypeError, ValueError):
        return None
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def compute_delivery_fee(restaurant_address, customer_address, subtotal):
    # Free delivery over threshold
    try:
        if float(subtotal) >= 50:
            return 0.0
    except Exception:
        pass

    # Distance-based calculation when coordinates exist
    if (
        getattr(restaurant_address, 'latitude', None) is not None and
        getattr(restaurant_address, 'longitude', None) is not None and
        getattr(customer_address, 'latitude', None) is not None and
        getattr(customer_address, 'longitude', None) is not None
    ):
        dist_km = _haversine_km(
            restaurant_address.latitude,
            restaurant_address.longitude,
            customer_address.latitude,
            customer_address.longitude,
        )
        if dist_km is not None:
            base = 1.50
            per_km = 0.50
            fee = base + per_km * max(0.0, dist_km)
            # Cap fee to a reasonable max
            return round(min(fee, 12.0), 2)

    # Fallback flat fee
    return 2.50


