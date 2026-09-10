# Importa o módulo responsável pela leitura de ficheiros CSV.
import csv

# Importa a classe base para criar comandos personalizados do Django.
from django.core.management.base import BaseCommand

# Importa o modelo Produto da aplicação api.
from api.models import Produto


# Define o comando personalizado para importar produtos.
class Command(BaseCommand):
    # Descrição apresentada pelo Django para este comando.
    help = 'Importa dados de produtos via CSV'

    # Método executado quando o comando é chamado no terminal.
    def handle(self, *args, **kwargs):
        # Define o nome do ficheiro CSV localizado na raiz do projeto.
        caminho = 'bi_products.csv'

        try:
            # Abre o ficheiro CSV com suporte para caracteres UTF-8.
            with open(caminho, mode='r', encoding='utf-8-sig') as ficheiro:
                # Cria um leitor que transforma cada linha num dicionário.
                leitor = csv.DictReader(ficheiro)

                # Inicializa o contador de produtos importados.
                contador = 0

                # Percorre todas as linhas do ficheiro CSV.
                for linha in leitor:
                    # Cria ou atualiza o produto através do ProductID.
                    # Esta operação evita a duplicação de registos.
                    Produto.objects.update_or_create(
                        product_id=linha['ProductID'],
                        defaults={
                            # Converte o preço para número inteiro quando preenchido.
                            'unit_price': (
                                int(float(linha['UnitPrice']))
                                if linha.get('UnitPrice')
                                else None
                            ),

                            # Define a categoria do produto.
                            'category': linha['Category'],

                            # Define o nome do produto.
                            'product_name': linha['ProductName']
                        }
                    )

                    # Incrementa o número de produtos processados.
                    contador += 1

            # Apresenta uma mensagem de sucesso após a importação.
            self.stdout.write(
                self.style.SUCCESS(
                    f'Sucesso! {contador} produtos importados.'
                )
            )

        # Trata o caso em que o ficheiro CSV não foi encontrado.
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    f'Ficheiro {caminho} não encontrado. '
                    'Coloque-o junto ao manage.py.'
                )
            )