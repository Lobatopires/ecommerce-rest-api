# Importa as ferramentas de serialização do Django REST Framework.
from rest_framework import serializers

# Importa os modelos que serão convertidos para JSON e vice-versa.
from .models import Cliente, Produto, Pedido, Pagamento


# Serializer responsável pelos dados dos clientes.
class ClienteSerializer(serializers.ModelSerializer):
    # Define a configuração do serializer.
    class Meta:
        # Indica o modelo associado.
        model = Cliente

        # Inclui todos os campos do modelo.
        fields = '__all__'


# Serializer responsável pelos dados dos produtos.
class ProdutoSerializer(serializers.ModelSerializer):
    # Define a configuração do serializer.
    class Meta:
        # Indica o modelo associado.
        model = Produto

        # Inclui todos os campos do modelo.
        fields = '__all__'


# Serializer responsável pelos dados dos pedidos.
class PedidoSerializer(serializers.ModelSerializer):
    # Define a configuração do serializer.
    class Meta:
        # Indica o modelo associado.
        model = Pedido

        # Inclui todos os campos do modelo.
        fields = '__all__'


# Serializer responsável pelos dados dos pagamentos.
class PagamentoSerializer(serializers.ModelSerializer):
    # Define a configuração do serializer.
    class Meta:
        # Indica o modelo associado.
        model = Pagamento

        # Inclui todos os campos do modelo.
        fields = '__all__'