# Importa o módulo responsável pela leitura de ficheiros CSV.
import csv

# Importa a classe base para criar comandos personalizados do Django.
from django.core.management.base import BaseCommand

# Importa o modelo Pedido da aplicação api.
from api.models import Pedido


# Define o comando personalizado de importação de pedidos.
class Command(BaseCommand):
    # Descrição apresentada pelo Django para este comando.
    help = 'Importa dados de pedidos via CSV'

    # Método executado quando o comando é chamado no terminal.
    def handle(self, *args, **kwargs):
        # Define o nome e o caminho do ficheiro CSV a importar.
        caminho = 'bi_orders.csv'

        # Inicializa o contador antes do bloco try.
        contador = 0

        try:
            # Abre o ficheiro CSV com suporte para caracteres UTF-8.
            with open(caminho, mode='r', encoding='utf-8-sig') as ficheiro:
                # Cria um leitor que transforma cada linha num dicionário.
                leitor = csv.DictReader(ficheiro)

                # Percorre todas as linhas do ficheiro CSV.
                for linha in leitor:
                    # Obtém e limpa a data do pedido.
                    data_bruta = linha.get('OrderDate', '').strip()

                    # Usa None quando a data estiver vazia.
                    data_final = data_bruta if data_bruta else None

                    # Obtém a quantidade do pedido.
                    qtd_bruta = linha.get('Quantity', '').strip()

                    # Converte a quantidade para inteiro.
                    # Define 1 caso o campo esteja vazio.
                    qtd = int(float(qtd_bruta)) if qtd_bruta else 1

                    # Obtém o valor do desconto.
                    desc_bruto = linha.get('Discount', '').strip()

                    # Converte o desconto para número decimal.
                    # Define 0.00 caso o campo esteja vazio.
                    desc = float(desc_bruto) if desc_bruto else 0.00

                    # Cria ou atualiza o pedido através do OrderID.
                    Pedido.objects.update_or_create(
                        order_id=linha['OrderID'],
                        defaults={
                            # Define o cliente associado ao pedido.
                            'customer_id': linha['CustomerID'],

                            # Define o produto associado ao pedido.
                            'product_id': linha['ProductID'],

                            # Define a data do pedido.
                            'order_date': data_final,

                            # Define a quantidade encomendada.
                            'quantity': qtd,

                            # Define o desconto aplicado.
                            'discount': desc,

                            # Define o método de pagamento.
                            'payment_method': linha.get('PaymentMethod', ''),

                            # Define o estado do pedido.
                            'status': linha.get('Status', '')
                        }
                    )

                    # Incrementa o número de pedidos processados.
                    contador += 1

            # Apresenta uma mensagem de sucesso após a importação.
            self.stdout.write(
                self.style.SUCCESS(
                    f'Sucesso! {contador} pedidos importados.'
                )
            )

        # Trata o caso em que o ficheiro CSV não foi encontrado.
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    f'Ficheiro {caminho} não encontrado.'
                )
            )

        # Trata outros erros ocorridos durante a importação.
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Erro na linha {contador + 1}: {str(e)}'
                )
            )