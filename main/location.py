import json
from shapely.geometry import Point, Polygon
from .models import ServiceableArea, Address

class LocationService:
    @staticmethod
    def is_location_serviceable(address):
        # If we have coordinates, check against serviceable areas
        if address.latitude and address.longitude:
            point = Point(address.latitude, address.longitude)
            
            # Check all active serviceable areas
            serviceable_areas = ServiceableArea.objects.filter(is_active=True)
            
            for area in serviceable_areas:
                # Parse the polygon coordinates from the stored format
                # Assuming it's stored as a GeoJSON-like format
                try:
                    coordinates = json.loads(area.polygon_coordinates)
                    polygon = Polygon(coordinates)
                    
                    # Check if the point is within the polygon
                    if polygon.contains(point):
                        return True
                except Exception as e:
                    # Log the error but continue checking other areas
                    print(f"Error checking area {area.name}: {str(e)}")
            
            # If we've checked all areas and none contain the point
            return False
        
        # If we don't have coordinates, fall back to checking by postal code or city
        # This is a simplified approach
        serviceable_postal_codes = ['12345', '23456', '34567']  # Example list
        serviceable_cities = ['City A', 'City B', 'City C']  # Example list
        
        if address.postal_code in serviceable_postal_codes or address.city in serviceable_cities:
            return True
        
        return False
    
    @staticmethod
    def check_and_update_address_serviceability(address):
        is_serviceable = LocationService.is_location_serviceable(address)
        
        # Update the address serviceability status if it has changed
        if address.is_serviceable != is_serviceable:
            address.is_serviceable = is_serviceable
            address.save()
        
        return is_serviceable