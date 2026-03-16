from django.core.management.base import BaseCommand
from orders.models import Order, OrderItem, MenuItem

class Command(BaseCommand):
    help = 'Seed the database with initial orders'

    def handle(self, *args, **options):
        # Clear existing orders if any
        Order.objects.all().delete()

        # Get some menu items
        bruschetta = MenuItem.objects.get(name='Bruschetta')
        salada = MenuItem.objects.get(name='Salada de Tomate')
        sopa = MenuItem.objects.get(name='Sopa de Legumes')
        bife = MenuItem.objects.get(name='Bife à Portuguesa')
        bacalhau = MenuItem.objects.get(name='Bacalhau à Brás')
        pudim = MenuItem.objects.get(name='Pudim')

        # Sample orders
        orders_data = [
            {
                'table_number': 1,
                'status': 'ORDER_PREVIEW',
                'items': [
                    {'menu_item': bruschetta, 'quantity': 2},
                    {'menu_item': salada, 'quantity': 1},
                ]
            },
            {
                'table_number': 2,
                'status': 'PREPARING',
                'items': [
                    {'menu_item': sopa, 'quantity': 1},
                    {'menu_item': bife, 'quantity': 1},
                ]
            },
            {
                'table_number': 3,
                'status': 'COOLING_DOWN',
                'items': [
                    {'menu_item': bacalhau, 'quantity': 2},
                ]
            },
            {
                'table_number': 4,
                'status': 'READY_TO_SERVE',
                'items': [
                    {'menu_item': bife, 'quantity': 1},
                    {'menu_item': pudim, 'quantity': 1},
                ]
            },
            {
                'table_number': 5,
                'status': 'CONCLUDED',
                'items': [
                    {'menu_item': salada, 'quantity': 1},
                    {'menu_item': sopa, 'quantity': 1},
                    {'menu_item': bacalhau, 'quantity': 1},
                ]
            },
        ]

        for order_data in orders_data:
            items = order_data.pop('items')
            order = Order.objects.create(**order_data)
            for item in items:
                OrderItem.objects.create(order=order, **item)
            self.stdout.write(self.style.SUCCESS(f'Created order for table {order.table_number} with status {order.status}'))

        self.stdout.write(self.style.SUCCESS('Orders seeded successfully!'))