from django.core.management.base import BaseCommand
from orders.models import MenuItem

class Command(BaseCommand):
    help = 'Seed the database with initial menu items'

    def handle(self, *args, **options):
        # Clear existing menu items if any
        MenuItem.objects.all().delete()

        # Sample menu items for each category
        menu_items = [
            {
                'name': 'Bruschetta',
                'category': 'ENTRADAS',
                'description': 'Pão torrado com tomate, manjericão e azeite',
                'ingredients': 'Pão italiano, tomate, manjericão, azeite de oliva, alho'
            },
            {
                'name': 'Salada de Tomate',
                'category': 'ENTRADAS',
                'description': 'Tomates frescos com cebola e ervas',
                'ingredients': 'Tomate, cebola roxa, azeite, vinagre, sal, pimenta'
            },
            {
                'name': 'Sopa de Legumes',
                'category': 'SOPAS',
                'description': 'Sopa saudável com vários legumes',
                'ingredients': 'Cenoura, batata, cebola, alho, caldo de legumes, ervas'
            },
            {
                'name': 'Caldo Verde',
                'category': 'SOPAS',
                'description': 'Sopa tradicional portuguesa com couve',
                'ingredients': 'Batata, couve galega, chouriço, azeite, alho'
            },
            {
                'name': 'Bife à Portuguesa',
                'category': 'CARNE',
                'description': 'Bife com molho de vinho e batatas fritas',
                'ingredients': 'Bife de vaca, vinho tinto, batatas, cebola, alho, louro'
            },
            {
                'name': 'Frango Assado',
                'category': 'CARNE',
                'description': 'Frango assado com ervas e limão',
                'ingredients': 'Frango inteiro, limão, alecrim, tomilho, azeite, sal'
            },
            {
                'name': 'Bacalhau à Brás',
                'category': 'PEIXE',
                'description': 'Bacalhau desfiado com batatas e ovos',
                'ingredients': 'Bacalhau, batatas, ovos, cebola, azeite, salsa'
            },
            {
                'name': 'Salmão Grelhado',
                'category': 'PEIXE',
                'description': 'Salmão fresco grelhado com legumes',
                'ingredients': 'Salmão, limão, ervas, azeite, sal, pimenta'
            },
            {
                'name': 'Pudim',
                'category': 'SOBREMESA',
                'description': 'Pudim de leite cremoso',
                'ingredients': 'Leite, ovos, açúcar, baunilha'
            },
            {
                'name': 'Tarte de Maçã',
                'category': 'SOBREMESA',
                'description': 'Tarte crocante com maçãs frescas',
                'ingredients': 'Maçãs, massa folhada, açúcar, canela, manteiga'
            },
        ]

        for item in menu_items:
            MenuItem.objects.create(**item)
            self.stdout.write(self.style.SUCCESS(f'Created menu item: {item["name"]}'))

        self.stdout.write(self.style.SUCCESS('Menu seeded successfully!'))