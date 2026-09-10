# Importa o módulo para leitura e escrita de ficheiros CSV.
import csv

# Importa o módulo para verificar se um ficheiro já existe.
import os

# Importa a classe base para criar comandos personalizados do Django.
from django.core.management.base import BaseCommand

# Importa o modelo Pagamento da aplicação api.
from api.models import Pagamento


# Define o comando personalizado para importar pagamentos.
class Command(BaseCommand):
    # Descrição apresentada pelo Django para este comando.
    help = 'Importa dados de Pagamentos e adiciona log de rejeitados sem apagar os antigos'

    # Método executado quando o comando é chamado no terminal.
    def handle(self, *args, **kwargs):
        # Define o ficheiro CSV de origem.
        caminho_origem = 'bi_payments.csv'

        # Define o ficheiro onde serão registados os pagamentos rejeitados.
        caminho_rejeitados = 'pagamentos_rejeitados.csv'

        try:
            # Verifica se o ficheiro de rejeitados já existe antes de o abrir.
            ficheiro_ja_existe = os.path.exists(caminho_rejeitados)

            # Abre o ficheiro de origem para leitura.
            # Abre o ficheiro de rejeitados em modo append, preservando os registos anteriores.
            with open(
                caminho_origem,
                mode='r',
                encoding='utf-8-sig'
            ) as ficheiro_lido, \
                 open(
                     caminho_rejeitados,
                     mode='a',
                     encoding='utf-8',
                     newline=''
                 ) as ficheiro_erro:

                # Lê cada linha do ficheiro CSV como um dicionário.
                leitor = csv.DictReader(ficheiro_lido)

                # Cria um escritor CSV com os mesmos campos do ficheiro de origem.
                escritor = csv.DictWriter(
                    ficheiro_erro,
                    fieldnames=leitor.fieldnames
                )

                # Escreve o cabeçalho apenas quando o ficheiro é criado pela primeira vez.
                if not ficheiro_ja_existe:
                    escritor.writeheader()

                # Inicializa o contador de pagamentos importados ou atualizados.
                sucesso = 0

                # Inicializa o contador de pagamentos rejeitados.
                ignorados = 0

                # Percorre todas as linhas do ficheiro CSV.
                for linha in leitor:
                    # Obtém a data do pagamento e remove espaços desnecessários.
                    data_bruta = linha.get('PaymentDate', '').strip()

                    # Usa None quando a data estiver vazia.
                    data_final = data_bruta if data_bruta else None

                    try:
                        # Cria ou atualiza o pagamento através do PaymentID.
                        Pagamento.objects.update_or_create(
                            payment_id=linha['PaymentID'],
                            defaults={
                                # Define o pedido associado ao pagamento.
                                'order_id': linha['OrderID'],

                                # Define a data do pagamento.
                                'payment_date': data_final,

                                # Define o estado do pagamento.
                                'payment_status': linha.get(
                                    'PaymentStatus',
                                    ''
                                )
                            }
                        )

                        # Incrementa o contador de operações concluídas.
                        sucesso += 1

                    except Exception:
                        # Regista no ficheiro de rejeitados a linha que originou o erro.
                        escritor.writerow(linha)

                        # Incrementa o contador de pagamentos rejeitados.
                        ignorados += 1

            # Apresenta o número de pagamentos importados ou atualizados.
            self.stdout.write(
                self.style.SUCCESS(
                    f'Sucesso! {sucesso} atualizados/importados.'
                )
            )

            # Apresenta o número de pagamentos rejeitados.
            self.stdout.write(
                self.style.WARNING(
                    f'Auditoria: {ignorados} pagamentos rejeitados '
                    f'(anexados em {caminho_rejeitados}).'
                )
            )

        # Trata o caso em que o ficheiro de origem não foi encontrado.
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    f'Ficheiro {caminho_origem} não encontrado.'
                )
            )