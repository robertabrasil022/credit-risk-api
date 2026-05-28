# 💳 Credit Risk Analysis API

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql)
![Pytest](https://img.shields.io/badge/Tests-7%20passed-brightgreen?logo=pytest)
![License](https://img.shields.io/badge/License-MIT-yellow)

> Microsserviço de análise de risco de crédito desenvolvido com FastAPI e PostgreSQL, simulando o core de sistemas utilizados em fintechs e bureaus de crédito como a Serasa Experian.

---

## 📋 Sobre o Projeto

Este projeto simula um microsserviço real de análise de risco de crédito, capaz de:

- Avaliar o perfil financeiro de clientes com base em score, renda e histórico de transações
- Classificar o risco em 4 níveis: `LOW`, `MEDIUM`, `HIGH` e `CRITICAL`
- Aprovar ou reprovar crédito automaticamente com base em algoritmo ponderado
- Expor os resultados via API REST documentada com ReDoc e Swagger UI

---

## 🏗️ Arquitetura

```
credit-risk-api/
├── app/
│   ├── api/
│   │   ├── routes.py        # Endpoints da API
│   │   └── schemas.py       # Schemas Pydantic de entrada/saída
│   ├── core/
│   │   └── config.py        # Configurações via variáveis de ambiente
│   ├── database/
│   │   ├── connection.py    # Conexão SQLAlchemy com PostgreSQL
│   │   └── models.py        # Modelos das tabelas do banco
│   └── services/
│       └── risk_service.py  # Algoritmo de análise de risco
├── scripts/
│   └── seed_data.py         # Geração de dados fictícios com Faker
├── tests/
│   └── test_risk_service.py # Testes unitários com Pytest
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt
└── .env.example
```

---

## 🧠 Algoritmo de Risco

O score de risco é calculado com pesos ponderados:

| Fator | Peso |
|---|---|
| Score de crédito (0–1000) | 50% |
| Renda mensal | 30% |
| Volume de transações | 20% |

Um fator de endividamento penaliza clientes com alto volume de gastos em relação à renda.

| Risk Score | Nível | Decisão |
|---|---|---|
| ≥ 0.75 | LOW | ✅ Aprovado |
| ≥ 0.50 | MEDIUM | ✅ Aprovado com reservas |
| ≥ 0.25 | HIGH | ❌ Reprovado |
| < 0.25 | CRITICAL | ❌ Reprovado |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.13+
- PostgreSQL 18+
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/robertabrasil022/credit-risk-api.git
cd credit-risk-api
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com suas credenciais do PostgreSQL
```

### 5. Crie o banco de dados
```bash
psql -U postgres -c "CREATE DATABASE credit_risk_db;"
```

### 6. Popule o banco com dados fictícios
```bash
python scripts/seed_data.py
```

### 7. Inicie a API
```bash
uvicorn main:app --reload
```

---

## 📡 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Health check do serviço |
| `GET` | `/clients/` | Lista todos os clientes |
| `GET` | `/clients/{id}` | Busca cliente com transações |
| `GET` | `/clients/{id}/analysis` | Retorna análise de risco do cliente |
| `POST` | `/clients/analyze` | Executa análise de risco em tempo real |

### Exemplo de requisição — Análise em tempo real

```bash
curl -X POST "http://localhost:8000/clients/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "credit_score": 820,
    "monthly_income": 8500.00,
    "total_transactions": 12,
    "total_transaction_amount": 3200.00
  }'
```

### Exemplo de resposta

```json
{
  "risk_level": "MEDIUM",
  "risk_score": 0.645,
  "approved": "YES",
  "analysis_notes": "Perfil de risco moderado. Aprovado com reservas. | Score: 820 | Renda: R$8500.00"
}
```

---

## 🧪 Testes

```bash
pytest tests/ -v
```

```
7 passed in 0.85s
```

---

## 🛠️ Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** — Framework web moderno e de alta performance
- **[PostgreSQL](https://www.postgresql.org/)** — Banco de dados relacional
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para mapeamento objeto-relacional
- **[Pydantic](https://docs.pydantic.dev/)** — Validação de dados e schemas
- **[Pytest](https://pytest.org/)** — Framework de testes automatizados
- **[Faker](https://faker.readthedocs.io/)** — Geração de dados fictícios realistas

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.