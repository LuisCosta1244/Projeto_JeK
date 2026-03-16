from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer

class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para listar itens do menu. 
    Permite filtrar por categoria (ex: /api/menu/?category=SOPAS)
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category.upper())
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    """
    Endpoint para criar, listar e atualizar pedidos.
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    # Sobrescrevemos o update parcial para facilitar a mudança de colunas na cozinha
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
