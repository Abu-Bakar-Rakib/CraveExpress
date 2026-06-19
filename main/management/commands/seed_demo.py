from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Restaurant, Address, MenuItem


class Command(BaseCommand):
    help = 'Seed 10 demo restaurants with diverse menu items'

    def _create_restaurant(self, user, name, address_line, city):
        rest, _ = Restaurant.objects.get_or_create(
            name=name,
            defaults={
                'description': f'{name} - great taste in {city}',
                'address': Address.objects.create(
                    user=user,
                    address_line=address_line, city=city, state='State X', postal_code='12345', is_default=True
                ),
                'phone_number': '+10000000000',
                'email': f'{name.lower().replace(" ", "")}@example.com',
                'opening_time': '08:00',
                'closing_time': '22:00',
            }
        )
        return rest

    def _add_items(self, rest, items):
        created = 0
        for name, category, price in items:
            _, was_created = MenuItem.objects.get_or_create(
                restaurant=rest, name=name,
                defaults={'description': name, 'category': category, 'price': price, 'is_available': True}
            )
            if was_created:
                created += 1
        return created

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username='restadmin', defaults={
            'email': 'owner@example.com', 'user_type': 'admin'
        })
        restaurant_specs = [
            ('City Bites', '123 Main St', 'City A'),
            ('Spice Route', '12 Oak Ave', 'City A'),
            ('Burger Barn', '88 King St', 'City B'),
            ('Pasta Palace', '9 River Rd', 'City B'),
            ('Sushi Central', '5 Cherry Ln', 'City C'),
            ('Taco Town', '44 Maple St', 'City C'),
            ('Veggie Delights', '3 Pine Rd', 'City D'),
            ('BBQ Shack', '21 Hill St', 'City D'),
            ('Curry Corner', '7 Lake Ave', 'City E'),
            ('Noodle House', '15 Garden St', 'City E'),
        ]

        default_items = [
            # foods
            ('Cheeseburger', 'food', 8.99),
            ('Grilled Chicken', 'food', 10.50),
            ('Margherita Pizza', 'food', 11.50),
            ('Pasta Alfredo', 'food', 12.00),
            ('Veggie Bowl', 'food', 9.25),
            # beverages
            ('Coke', 'drink', 1.99),
            ('Lemonade', 'drink', 2.50),
            ('Iced Tea', 'drink', 2.40),
            # desserts
            ('Chocolate Cake', 'dessert', 4.75),
            ('Ice Cream Scoop', 'dessert', 2.50),
            # combos
            ('Burger + Fries + Drink', 'combo', 12.99),
            ('Pizza Slice + Drink', 'combo', 6.99),
            ('Pasta + Garlic Bread + Drink', 'combo', 13.99),
        ]

        total_created = 0
        for name, addr, city in restaurant_specs:
            rest = self._create_restaurant(user, name, addr, city)
            total_created += self._add_items(rest, default_items)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(restaurant_specs)} restaurants and ~{total_created} menu items'))


