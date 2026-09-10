# E-Commerce Data API

API REST para gestao de clientes, produtos, pedidos e pagamentos, desenvolvida
com Django REST Framework e PostgreSQL.

## Requisitos

- Python 3.10 ou superior
- PostgreSQL
- `pip`

As dependencias Python utilizadas pelo projeto estao definidas em
`requirements.txt`:

```text
asgiref==3.12.1
attrs==26.1.0
Django==5.2.17
django-cors-headers==4.9.0
django-filter==26.1
djangorestframework==3.18.1
drf-spectacular==0.30.0
inflection==0.5.1
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
psycopg2-binary==2.9.12
python-dotenv==1.2.3
PyYAML==6.0.3
referencing==0.37.0
rpds-py==2026.6.3
sqlparse==0.6.0
typing_extensions==4.16.0
tzdata==2026.3
uritemplate==4.2.0
```

## Instalar o projeto

1. Clone o repositorio e entre na pasta do projeto.
2. Crie e ative um ambiente virtual:

	```powershell
	python -m venv venv
	.\venv\Scripts\Activate.ps1
	```

3. Instale as dependencias:

	```powershell
	pip install -r requirements.txt
	```

4. Crie um ficheiro `.env` na raiz do projeto com as credenciais da base de
	dados:

	```env
	SECRET_KEY=chave-secreta-do-django
	DB_NAME=ecommerce
	DB_USER=postgres
	DB_PASSWORD=senha-do-postgres
	DB_HOST=localhost
	DB_PORT=5432
	```

5. Crie a base de dados PostgreSQL indicada em `DB_NAME`.

## Preparar a base de dados

Execute as migracoes:

```powershell
python manage.py migrate
```

Para criar um utilizador administrador:

```powershell
python manage.py createsuperuser
```

## Importar dados CSV

Os ficheiros `bi_customers.csv`, `bi_products.csv`, `bi_orders.csv` e
`bi_payments.csv` devem permanecer na raiz do projeto, junto ao `manage.py`.

Execute os importadores nesta ordem para respeitar as relacoes entre os
registos:

```powershell
python manage.py import_clients
python manage.py import_products
python manage.py import_orders
python manage.py import_payments
```

Os importadores atualizam registos existentes em vez de os duplicarem. O
importador de pagamentos acrescenta linhas rejeitadas ao ficheiro
`pagamentos_rejeitados.csv`.

## Executar a API

```powershell
python manage.py runserver
```

Por defeito, a API fica disponivel em `http://127.0.0.1:8000/`.

## Endpoints

Todos os endpoints da API estao sob o prefixo `/api/` e requerem autenticacao.

| Recurso | Endpoint |
| --- | --- |
| Clientes | `/api/clientes/` |
| Produtos | `/api/produtos/` |
| Pedidos | `/api/pedidos/` |
| Pagamentos | `/api/pagamentos/` |

Cada recurso suporta as operacoes CRUD fornecidas pelo Django REST Framework:

- `GET` para listar e consultar
- `POST` para criar
- `PUT` e `PATCH` para atualizar
- `DELETE` para remover

### Filtros disponiveis

- Clientes: `age`, `age__gte`, `age__lte`, `city`, `city__icontains`,
  `customer_segment`, `signup_date`, `signup_date__gte` e `signup_date__lte`
- Produtos: `category`
- Pedidos: `customer_id` e `product_id`
- Pagamentos: `payment_status`

Exemplo:

```text
GET /api/clientes/?city__icontains=Lisboa
GET /api/pedidos/?customer_id=C001
```

## Autenticacao

A API utiliza autenticacao por token. Depois de criar um token para um
utilizador, envie-o nos pedidos:

```text
Authorization: Token <seu-token>
```

## Documentacao da API

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- Schema OpenAPI: `http://127.0.0.1:8000/api/schema/`
- Administracao Django: `http://127.0.0.1:8000/admin/`

## Testes

Execute os testes com:

```powershell
python manage.py test
```

## Estrutura principal

```text
api/       Aplicacao Django, modelos, serializers, views e importadores
setup/     Configuracao do projeto Django
manage.py  Utilitario de administracao do Django
*.csv      Dados de origem para importacao
```
