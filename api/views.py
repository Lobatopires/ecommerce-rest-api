# Importa as classes de ViewSet disponibilizadas pelo Django REST Framework.
from rest_framework import viewsets

# Importa o backend responsável pelos filtros dos endpoints.
from django_filters.rest_framework import DjangoFilterBackend

# Importa os modelos utilizados pelas views.
from .models import Cliente, Produto, Pedido, Pagamento

# Importa os serializers responsáveis por converter os dados para JSON.
from .serializers import (
    ClienteSerializer,
    ProdutoSerializer,
    PedidoSerializer,
    PagamentoSerializer,
)


# ViewSet responsável pelas operações sobre clientes.
class ClienteViewSet(viewsets.ModelViewSet):
    # Define todos os clientes como queryset da view.
    queryset = Cliente.objects.all()

    # Define o serializer utilizado para os clientes.
    serializer_class = ClienteSerializer

    # Ativa o sistema de filtragem do Django Filters.
    filter_backends = [DjangoFilterBackend]

    # Define os campos e os tipos de filtro permitidos.
    filterset_fields = {
        # Permite filtrar por idade exata, mínima ou máxima.
        'age': ['exact', 'gte', 'lte'],

        # Permite pesquisar uma cidade exata ou parcialmente.
        'city': ['exact', 'icontains'],

        # Permite filtrar pelo segmento exato do cliente.
        'customer_segment': ['exact'],

        # Permite filtrar por uma data exata ou por intervalo.
        'signup_date': ['exact', 'gte', 'lte'],
    }


# ViewSet responsável pelas operações sobre produtos.
class ProdutoViewSet(viewsets.ModelViewSet):
    # Define todos os produtos como queryset da view.
    queryset = Produto.objects.all()

    # Define o serializer utilizado para os produtos.
    serializer_class = ProdutoSerializer

    # Ativa o sistema de filtragem do Django Filters.
    filter_backends = [DjangoFilterBackend]

    # Permite filtrar produtos pela categoria.
    filterset_fields = ['category']


# ViewSet responsável pelas operações sobre pedidos.
class PedidoViewSet(viewsets.ModelViewSet):
    # Define todos os pedidos como queryset da view.
    queryset = Pedido.objects.all()

    # Define o serializer utilizado para os pedidos.
    serializer_class = PedidoSerializer

    # Ativa o sistema de filtragem do Django Filters.
    filter_backends = [DjangoFilterBackend]

    # Permite filtrar pelo cliente ou pelo produto associado.
    filterset_fields = ['customer_id', 'product_id']


# ViewSet responsável pelas operações sobre pagamentos.
class PagamentoViewSet(viewsets.ModelViewSet):
    # Define todos os pagamentos como queryset da view.
    queryset = Pagamento.objects.all()

    # Define o serializer utilizado para os pagamentos.
    serializer_class = PagamentoSerializer

    # Ativa o sistema de filtragem do Django Filters.
    filter_backends = [DjangoFilterBackend]

    # Permite filtrar pelo estado do pagamento.
    filterset_fields = ['payment_status']