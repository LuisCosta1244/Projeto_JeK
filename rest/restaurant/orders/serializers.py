from rest_framework import serializers
from .models import MenuItem, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    # Para leitura, queremos os detalhes do prato. Para escrita, apenas o ID.
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item_id', 'menu_item_details', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'status', 'created_at', 'items']
        read_only_fields = ['status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    
    # Adicionamos a capacidade de atualizar apenas o estado (movimentação no Kanban)
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
