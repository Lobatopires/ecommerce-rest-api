# Importa as classes necessárias para criar modelos e campos no Django.
from django.db import models


# Representa um cliente da aplicação.
class Cliente(models.Model):
    # Identificador único do cliente.
    # CharField permite valores alfanuméricos, como "C001".
    customer_id = models.CharField(
        max_length=50,
        primary_key=True
    )

    # Idade do cliente, podendo ficar vazia.
    age = models.IntegerField(
        null=True,
        blank=True
    )

    # Cidade onde o cliente reside.
    city = models.CharField(max_length=100)

    # Segmento comercial do cliente.
    customer_segment = models.CharField(max_length=50)

    # Data de registo do cliente, podendo ficar vazia.
    signup_date = models.DateField(
        null=True,
        blank=True
    )

    # Define a representação textual do cliente.
    def __str__(self):
        return self.customer_id


# Representa um produto da aplicação.
class Produto(models.Model):
    # Identificador único do produto.
    product_id = models.CharField(
        max_length=50,
        primary_key=True
    )

    # Categoria à qual o produto pertence.
    category = models.CharField(max_length=100)

    # Nome do produto.
    product_name = models.CharField(max_length=200)

    # Preço unitário do produto, com duas casas decimais.
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Define a representação textual do produto.
    def __str__(self):
        return self.product_name


# Representa um pedido realizado por um cliente.
class Pedido(models.Model):
    # Identificador único do pedido.
    order_id = models.CharField(
        max_length=50,
        primary_key=True
    )

    # Relaciona o pedido com um cliente.
    # Um cliente pode realizar vários pedidos.
    # PROTECT impede apagar um cliente com pedidos associados.
    customer = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )

    # Relaciona o pedido com um produto.
    # Um produto pode aparecer em vários pedidos.
    product = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )

    # Data e hora em que o pedido foi realizado.
    order_date = models.DateTimeField()

    # Quantidade de unidades incluídas no pedido.
    quantity = models.IntegerField(default=1)

    # Desconto aplicado ao pedido.
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    # Método de pagamento utilizado.
    payment_method = models.CharField(max_length=50)

    # Estado atual do pedido.
    status = models.CharField(max_length=50)

    # Define a representação textual do pedido.
    def __str__(self):
        return self.order_id


# Representa um pagamento associado a um pedido.
class Pagamento(models.Model):
    # Identificador único do pagamento.
    payment_id = models.CharField(
        max_length=50,
        primary_key=True
    )

    # Relaciona o pagamento com um único pedido.
    # Cada pedido pode ter apenas um pagamento.
    # CASCADE elimina o pagamento quando o pedido é eliminado.
    order = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='pagamento'
    )

    # Data e hora em que o pagamento foi efetuado.
    payment_date = models.DateTimeField()

    # Estado atual do pagamento.
    payment_status = models.CharField(max_length=50)

    # Define a representação textual do pagamento.
    def __str__(self):
        return self.payment_id