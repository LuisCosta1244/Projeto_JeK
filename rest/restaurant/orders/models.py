from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('ENTRADAS', 'Entradas'),
        ('SOPAS', 'Sopas'),
        ('CARNE', 'Carne'),
        ('PEIXE', 'Peixe'),
        ('SOBREMESA', 'Sobremesa')]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    ingredients = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('ORDER_PREVIEW', 'Order Preview'),
        ('PREPARING', 'Preparing'),
        ('COOLING_DOWN', 'Cooling Down'),
        ('READY_TO_SERVE', 'Ready to Serve'),
        ('CONCLUDED', 'Concluded')]

    table_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ORDER_PREVIEW')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mesa {self.table_number} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Pedido {self.order.id})"
