from datetime import datetime, timedelta
from django.db.models import Q, Count
from .models import DeliveryPersonnel, DeliverySchedule, Order, Address

class DeliveryManager:
    @staticmethod
    def get_available_delivery_personnel(delivery_time, delivery_address):
        # Get the day of the week for the delivery time
        day_of_week = delivery_time.strftime('%A').lower()
        
        # Find delivery personnel who are scheduled to work at the delivery time
        available_personnel = DeliveryPersonnel.objects.filter(
            is_available=True,
            schedules__date=delivery_time.date(),
            schedules__start_time__lte=delivery_time.time(),
            schedules__end_time__gte=delivery_time.time()
        )
        
        # Sort by current workload (number of active deliveries)
        available_personnel = available_personnel.annotate(
            active_deliveries=Count(
                'assigned_orders',
                filter=Q(assigned_orders__status__in=['confirmed', 'preparing', 'out_for_delivery'])
            )
        ).order_by('active_deliveries')
        
        # If location tracking is enabled, find the nearest delivery person
        if delivery_address.latitude and delivery_address.longitude:
            # This is a simplified approach - in a real system, you would use
            # geospatial queries or a distance calculation service
            for personnel in available_personnel:
                if personnel.current_location_lat and personnel.current_location_lng:
                    # Calculate rough distance (this is very simplified)
                    personnel.distance = ((personnel.current_location_lat - delivery_address.latitude) ** 2 + 
                                         (personnel.current_location_lng - delivery_address.longitude) ** 2) ** 0.5
            
            # Sort by distance if location is available
            available_personnel = sorted(
                [p for p in available_personnel if hasattr(p, 'distance')],
                key=lambda x: x.distance
            )
        
        return available_personnel
    
    @staticmethod
    def assign_delivery_person(order):
        # Estimate delivery time (30 minutes from now for this example)
        estimated_delivery_time = datetime.now() + timedelta(minutes=30)
        
        # Get available delivery personnel
        available_personnel = DeliveryManager.get_available_delivery_personnel(
            estimated_delivery_time, 
            order.delivery_address
        )
        
        if available_personnel:
            # Assign the first available delivery person
            order.delivery_person = available_personnel[0]
            order.estimated_delivery_time = estimated_delivery_time
            order.save()
            return True
        
        return False
    
    @staticmethod
    def generate_weekly_schedule():
        # This would typically be run as a scheduled task
        # Generate schedules for the next week for all delivery personnel
        delivery_personnel = DeliveryPersonnel.objects.all()
        
        # Start date for the schedule (next Monday)
        today = datetime.now().date()
        days_until_monday = (7 - today.weekday()) % 7
        start_date = today + timedelta(days=days_until_monday)
        
        for personnel in delivery_personnel:
            # Create a basic schedule - this would be more sophisticated in a real system
            for day in range(7):  # 7 days of the week
                current_date = start_date + timedelta(days=day)
                
                # Example: Create two shifts per day
                # Morning shift: 8 AM - 2 PM
                DeliverySchedule.objects.create(
                    delivery_person=personnel,
                    date=current_date,
                    start_time=datetime.strptime('08:00', '%H:%M').time(),
                    end_time=datetime.strptime('14:00', '%H:%M').time()
                )
                
                # Evening shift: 4 PM - 10 PM
                DeliverySchedule.objects.create(
                    delivery_person=personnel,
                    date=current_date,
                    start_time=datetime.strptime('16:00', '%H:%M').time(),
                    end_time=datetime.strptime('22:00', '%H:%M').time()
                )