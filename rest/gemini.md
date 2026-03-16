Boa! Isolar o projeto num ambiente virtual é uma excelente prática e será muito útil quando fores escrever as instruções de instalação no teu `README.md` (um dos requisitos da entrega).

Aqui tens o passo a passo para criares e configurares o teu ambiente Python:

### 1. Criar o Ambiente Virtual

Abre o teu terminal, navega até à pasta onde queres guardar o teu projeto e executa o seguinte comando. Isto vai criar uma pasta chamada `venv` que conterá o teu ambiente isolado:

**No Windows, macOS ou Linux:**

```bash
python -m venv venv

```

*(Nota: Se estiveres no macOS/Linux e o comando acima não funcionar, tenta usar `python3 -m venv venv`)*

---

### 2. Ativar o Ambiente Virtual

Antes de instalares qualquer coisa, precisas de "entrar" nesse ambiente. O comando varia consoante o teu sistema operativo:

**No Windows (Command Prompt / PowerShell):**

```bash
venv\Scripts\activate

```

**No macOS ou Linux:**

```bash
source venv/bin/activate

```

*Vais saber que funcionou porque o teu terminal vai passar a ter um `(venv)` no início da linha de comandos.*

---

### 3. Instalar as Dependências

Agora que estás dentro do ambiente virtual, vamos instalar o Django e o Django REST Framework (DRF):

```bash
pip install django djangorestframework django-cors-headers

```

---

### 4. Guardar as Dependências (Crucial para a Entrega)

Como o avaliador vai precisar de correr o teu código localmente, tens de lhe dizer que pacotes instalar. Podes gerar um ficheiro `requirements.txt` automaticamente com este comando:

```bash
pip freeze > requirements.txt

```

No teu `README.md`, poderás depois dizer ao avaliador para simplesmente correr `pip install -r requirements.txt`.

---

**Queres que avancemos agora para a criação da estrutura inicial de pastas e ficheiros do Django, ou queres começar a desenhar os modelos na base de dados?**


Excelente escolha! O Django é uma framework robusta e perfeita para este desafio, permitindo construir a API REST de forma rápida e segura.

Vou guiar-te passo a passo na implementação do **Backend** utilizando **Django** e **Django REST Framework (DRF)**. Esta base garante um modelo de dados limpo, normalizado e uma API REST que cumpre todos os requisitos do PDF.

Aqui está a arquitetura e o código essencial para o teu projeto.

---

### 1. Configuração Inicial

Primeiro, certifica-te de que tens o Django e o Django REST Framework instalados. No teu terminal:

```bash
pip install django djangorestframework django-cors-headers
django-admin startproject restaurant
cd restaurant
django-admin startapp orders

```

Adiciona `rest_framework`, `corsheaders` e a tua app `orders` ao `INSTALLED_APPS` no `settings.py`. Configura também o `CORS_ALLOWED_ORIGINS` para permitir que o teu frontend (ex: React) comunique com a API.

---

### 2. Modelo de Dados (`orders/models.py`)

O modelo de dados precisa de representar os itens do menu, os pedidos e as linhas de pedido. Aqui estruturamos as 5 categorias fixas e as fases do Kanban do dashboard da cozinha.

```python
from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('ENTRADAS', 'Entradas'),
        ('SOPAS', 'Sopas'),
        ('CARNE', 'Carne'),
        ('PEIXE', 'Peixe'),
        ('SOBREMESA', 'Sobremesa'),
    [cite_start]] # [cite: 17, 18, 19, 20, 21]

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
        ('CONCLUDED', 'Concluded'),
    [cite_start]] # [cite: 38]

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

```

---

### 3. Serializadores (`orders/serializers.py`)

Os serializadores convertem os modelos do Django para JSON. O desafio principal aqui é permitir a criação de um pedido (`Order`) juntamente com os seus itens (`OrderItem`) num único pedido (nested creation).

```python
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

```

---

### 4. Views da API (`orders/views.py`)

Vamos criar os endpoints necessários para o frontend consultar o menu, submeter pedidos e atualizar o estado no dashboard.

```python
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

```

---

### 5. Configuração de URLs (`orders/urls.py` e `restaurant/urls.py`)

No ficheiro `orders/urls.py` (cria este ficheiro):

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'menu', MenuItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```

No ficheiro principal `restaurant/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')), # O prefixo 'api/' garante boas convenções REST
]

```

---

### O que precisas de fazer a seguir para a tua entrega:

1. 
**Migrações:** Executa `python manage.py makemigrations` e `python manage.py migrate` para criar a base de dados SQLite recomendada.


2. **Popular o Menu:** Cria um script de seed ou usa o Django Admin (`python manage.py createsuperuser`) para adicionar os pratos base nas categorias exigidas.
3. **Frontend (React/JS):** Tens agora uma API pronta a receber chamadas (`GET /api/menu/`, `POST /api/orders/`, `PATCH /api/orders/{id}/`). O frontend deve consumir isto.


4. 
**Justificação (README):** Não te esqueças que uma das partes mais avaliadas é a justificação das tuas escolhas. No teu README, deves explicar porque usaste DRF (ex: serialização rápida, facilidade de criar padrões REST), e porque estruturaste as views desta forma.



Gostarias que eu detalhasse a estrutura inicial dos componentes React para o Frontend, ou preferes explorar a secção de Bónus e implementar o Tempo Real (WebSockets/SSE) no Django?
