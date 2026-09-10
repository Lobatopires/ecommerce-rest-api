# Importa o módulo de administração do Django.
from django.contrib import admin

# Importa os modelos que serão registados no painel administrativo.
from .models import Cliente, Produto, Pedido, Pagamento


# Regista e configura o modelo Cliente no painel administrativo.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Define as colunas apresentadas na tabela de clientes.
    list_display = (
        'customer_id',
        'city',
        'age',
        'customer_segment',
        'signup_date'
    )

    # Define os campos disponíveis para pesquisa.
    search_fields = ('customer_id', 'city')

    # Adiciona filtros laterais por segmento de cliente.
    list_filter = ('customer_segment',)


# Regista e configura o modelo Produto no painel administrativo.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Define as colunas apresentadas na tabela de produtos.
    list_display = ('product_id', 'category', 'unit_price')

    # Define os campos disponíveis para pesquisa.
    search_fields = ('product_id', 'category')

    # Adiciona um filtro lateral por categoria.
    list_filter = ('category',)


# Regista e configura o modelo Pedido no painel administrativo.
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Define as colunas apresentadas na tabela de pedidos.
    list_display = ('order_id', 'customer', 'product', 'order_date')

    # Permite pesquisar pelo identificador do pedido
    # e pelo identificador do cliente relacionado.
    search_fields = ('order_id', 'customer__customer_id')


# Regista e configura o modelo Pagamento no painel administrativo.
@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    # Define as colunas apresentadas na tabela de pagamentos.
    list_display = (
        'payment_id',
        'order',
        'payment_status',
        'payment_date'
    )

    # Adiciona um filtro lateral pelo estado do pagamento.
    list_filter = ('payment_status',)