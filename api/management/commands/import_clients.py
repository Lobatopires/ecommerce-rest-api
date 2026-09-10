# Importa o módulo para leitura de ficheiros CSV.
import csv

# Importa a classe base para criar comandos personalizados do Django.
from django.core.management.base import BaseCommand

# Importa o modelo Cliente da aplicação api.
from api.models import Cliente


# Define o comando personalizado para importar clientes.
class Command(BaseCommand):
    # Descrição apresentada pelo Django para este comando.
    help = 'Importa dados de clientes via CSV'

    # Método executado quando o comando é chamado no terminal.
    def handle(self, *args, **kwargs):
        # Define o nome do ficheiro CSV localizado na raiz do projeto.
        caminho = 'bi_customers.csv'

        try:
            # Abre o ficheiro CSV com suporte para caracteres UTF-8.
            with open(caminho, mode='r', encoding='utf-8-sig') as ficheiro:
                # Cria um leitor que transforma cada linha num dicionário.
                leitor = csv.DictReader(ficheiro)

                # Inicializa o contador de clientes importados.
                contador = 0

                # Percorre todas as linhas do ficheiro CSV.
                for linha in leitor:
                    # Obtém a data de registo e remove espaços desnecessários.
                    data_bruta = linha.get('SignupDate', '').strip()

                    # Usa None quando a data estiver vazia.
                    data_final = data_bruta if data_bruta else None

                    # Cria ou atualiza o cliente através do CustomerID.
                    # Esta operação evita a duplicação de registos.
                    Cliente.objects.update_or_create(
                        customer_id=linha['CustomerID'],
                        defaults={
                            # Converte a idade para inteiro quando o campo estiver preenchido.
                            'age': int(float(linha['Age'])) if linha.get('Age') else None,

                            # Define a cidade do cliente.
                            'city': linha['City'],

                            # Define o segmento do cliente.
                            'customer_segment': linha['CustomerSegment'],

                            # Define a data de registo do cliente.
                            'signup_date': data_final
                        }
                    )

                    # Incrementa o número de clientes processados.
                    contador += 1

            # Apresenta uma mensagem de sucesso após a importação.
            self.stdout.write(
                self.style.SUCCESS(
                    f'Sucesso! {contador} clientes importados.'
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