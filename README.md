# 🏢 Serviço Principal (Admin/Backoffice) - Tech Challenge Fase 4

Este repositório contém o microsserviço responsável pelo **Gerenciamento de Estoque (Backoffice)** da plataforma de revenda de veículos.

Sua principal responsabilidade é permitir o cadastro e edição de veículos e **sincronizar esses dados via HTTP** com o microsserviço de Vendas (Storefront), garantindo que a vitrine esteja sempre atualizada.

## 📋 Funcionalidades

* **Gestão de Veículos:**
    * Cadastro de novos veículos (Marca, Modelo, Ano, Cor, Preço).
    * Edição de dados de veículos existentes.
* **Integração entre Microsserviços:**
    * [cite_start]Disparo automático de requisições HTTP (POST) para a API de Vendas sempre que um veículo é cadastrado[cite: 14].
    * Arquitetura resiliente: O sistema salva no banco local mesmo se a integração falhar (tratamento de exceções).
* **Banco de Dados Isolado:**
    * [cite_start]Utiliza uma instância própria de PostgreSQL, segregada do serviço de vendas[cite: 22].

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Framework:** FastAPI (Alta performance e documentação automática).
* **ORM:** SQLAlchemy (Gerenciamento do banco de dados).
* **Banco de Dados:** PostgreSQL (Rodando em container Docker).
* **Integração:** Biblioteca `requests` para comunicação HTTP.
* **Testes:** Pytest & Pytest-cov (Cobertura > 80%).
* **Infraestrutura:** Docker & Docker Compose.

---

## 📂 Estrutura do Projeto

```text
tech-challenge-fase4-admin/
├── .github/workflows/   # Pipeline de CI/CD (GitHub Actions) [cite: 27]
├── src/
│   ├── routers/         # Endpoints (Admin Controller)
│   ├── config.py        # Configurações e Variáveis de Ambiente
│   ├── database.py      # Conexão com Banco de Dados
│   ├── main.py          # Inicialização da App
│   ├── models.py        # Tabela 'veiculos_admin'
│   └── schemas.py       # Validação Pydantic (Request/Response)
├── tests/               # Testes Automatizados (com Mock de HTTP)
├── docker-compose.yml   # Definição dos serviços (API Admin + DB Admin)
├── Dockerfile           # Imagem da aplicação
└── requirements.txt     # Dependências do projeto
```


---
🚀 Como Rodar o Projeto
-----------------------

Utilize o Docker para garantir que o ambiente suba com as configurações de rede e banco de dados corretas.

### Pré-requisitos

-   Docker e Docker Compose instalados.

-   *(Opcional)* O serviço de Vendas rodando para testar a integração real.

### Passo a Passo (Via Docker)

1.  **Clone o repositório:**

    Bash

    ```
    git clone <url-do-seu-repo-admin>
    cd tech-challenge-fase4-admin

    ```

2.  Suba o ambiente:

    Este comando sobe a API na porta 8001 e o Banco na porta 5433 (para não conflitar com o serviço de vendas).

    Bash

    ```
    docker-compose up --build

    ```

3.  Acesse a Documentação:

    Abra no navegador: http://localhost:8001/docs

4.  **Parar a execução:**

    Bash

    ```
    docker-compose down

    ```

### ⚙️ Configuração de Integração

No arquivo `docker-compose.yml` ou `.env`, a variável `VENDAS_API_URL` define para onde os dados serão enviados.

-   **Default Docker:** `http://api_vendas_container:8000/vendas/veiculos` (Assume que ambos estão na mesma rede Docker).

-   **Localhost:** Se rodar fora do Docker, ajuste para `http://localhost:8000/vendas/veiculos`.

* * * * *

🧪 Testes Automatizados
-----------------------

O projeto utiliza **Pytest** com **Mocking** para simular as requisições HTTP. Isso permite testar o Admin mesmo sem o serviço de Vendas estar rodando, garantindo isolamento.

### Executando os Testes

Para validar a lógica e verificar a cobertura de código (Requisito: 80% ^1^):

1.  **Via Docker (Recomendado):**

    Bash

    ```
    docker exec -it api_admin_container pytest --cov=src tests/

    ```

2.  **Localmente:**

    Bash

    ```
    pip install -r requirements.txt
    pytest --cov=src tests/

    ```

3.  **Gerar Relatório HTML:**

    Bash

    ```
    pytest --cov=src --cov-report=html tests/

    ```

    *Abra a pasta `htmlcov/index.html` para ver os detalhes.*

* * * * *

🔌 Endpoints Principais
-----------------------

### Admin (`/admin`)

-   **`POST /admin/veiculos`**:

    -   Cadastra um veículo no banco `admin_db`.

    -   **Trigger:** Tenta enviar um POST para a API de Vendas.

    -   *Payload Exemplo:*

        JSON

        ```
        {
          "marca": "Toyota",
          "modelo": "Corolla",
          "ano": 2024,
          "cor": "Preto",
          "preco": 150000
        }

        ```

-   **`PUT /admin/veiculos/{id}`**:

    -   Atualiza dados do veículo no banco local.

* * * * *

🐳 Resumo de Portas e Serviços
------------------------------

| **Serviço** | **Porta Host** | **Porta Container** | **Banco de Dados** |
| --- | --- | --- | --- |
| **API Admin** | `8001` | `8001` | `admin_db` (Porta 5433) |
| **API Vendas** | `8000` | `8000` | `vendas_db` (Porta 5432) |


---
**Nota:** Para o teste de integração completo funcionar, certifique-se de que o container `api_vendas_container` esteja rodando na mesma rede ou acessível via URL configurada.