# Store API (FastAPI + MongoDB + TDD)

API para gerenciamento de produtos utilizando FastAPI, MongoDB e Test-Driven Development (TDD).


## Requisitos

Python 3.10+

MongoDB rodando (local ou em Docker)

Pip (gerenciador de pacotes)


## Instalação

Clone o repositório:

git clone https://github.com/ronald-02/store-api.git
cd store-api


Crie e ative um ambiente virtual:

python -m venv venv



Instale as dependências:

pip install -r requirements.txt

## Executando a API

Certifique-se de que o MongoDB está rodando localmente (mongodb://localhost:27017).

Se preferir usar Docker:

docker run -d --name mongodb -p 27017:27017 mongo


Inicie a aplicação:

uvicorn app.main:app --reload


Acesse a documentação interativa:

Swagger UI → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

# Endpoints


Criar Produto

```POST /products

{
  "name": "Notebook Gamer",
  "description": "RTX 3060, i7, 16GB RAM",
  "price": 7500.00
}


Listar Produtos
GET /products


Com filtros opcionais:

GET /products?min_price=5000&max_price=10000


Buscar Produto por ID
GET /products/{id}


Atualizar Produto (total)
PUT /products/{id}


Corpo (JSON):

{
  "name": "Notebook Gamer Atualizado",
  "description": "RTX 3070, i9, 32GB RAM",
  "price": 8200.00
}


Atualizar Produto (parcial)
PATCH /products/{id}


Corpo (JSON):

{
  "price": 7000.00
}


Deletar Produto
DELETE /products/{id}


Rodando os Testes

Com o ambiente virtual ativado:

pytest -v


Você verá a saída com todos os testes marcados com @pytest.mark.asyncio.

Exemplo:

@pytest.mark.asyncio
async def test_create_product():
    ...
