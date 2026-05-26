import sys
import os

# Garante que o Python encontra os módulos do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from sqlalchemy.orm import Session
from app.database.connection import engine, Base
from app.database.models import Client, Transaction, CreditAnalysis, RiskLevel
import random

# Faker configurado para dados brasileiros
fake = Faker("pt_BR")
random.seed(42)  # Garante que os dados são sempre iguais ao rodar novamente

TRANSACTION_TYPES = ["compra", "saque", "transferencia", "pagamento", "deposito"]
MERCHANT_CATEGORIES = ["alimentacao", "viagem", "eletronicos", "saude", "educacao", "lazer"]


def generate_cpf() -> str:
    """Gera um CPF formatado fictício."""
    numbers = [random.randint(0, 9) for _ in range(11)]
    return f"{''.join(map(str, numbers[:3]))}.{''.join(map(str, numbers[3:6]))}.{''.join(map(str, numbers[6:9]))}-{''.join(map(str, numbers[9:]))}"


def calculate_risk(credit_score: int, monthly_income: float, transactions: list) -> tuple:
    """
    Calcula o risco de crédito baseado em:
    - Score de crédito (peso 50%)
    - Renda mensal (peso 30%)
    - Volume de transações (peso 20%)
    """
    # Normaliza score (0 a 1000) para 0.0 a 1.0
    score_factor = credit_score / 1000

    # Normaliza renda (até R$20.000) para 0.0 a 1.0
    income_factor = min(monthly_income / 20000, 1.0)

    # Normaliza transações (até 20) para 0.0 a 1.0
    transaction_factor = min(len(transactions) / 20, 1.0)

    # Calcula risk_score final (quanto MAIOR, menor o risco)
    risk_score = (score_factor * 0.5) + (income_factor * 0.3) + (transaction_factor * 0.2)

    # Define nível de risco
    if risk_score >= 0.75:
        return RiskLevel.LOW, risk_score, "YES"
    elif risk_score >= 0.50:
        return RiskLevel.MEDIUM, risk_score, "YES"
    elif risk_score >= 0.25:
        return RiskLevel.HIGH, risk_score, "NO"
    else:
        return RiskLevel.CRITICAL, risk_score, "NO"


def seed(db: Session):
    """Popula o banco com dados fictícios."""

    print("🌱 Iniciando seed do banco de dados...")

    # Limpa dados anteriores
    db.query(CreditAnalysis).delete()
    db.query(Transaction).delete()
    db.query(Client).delete()
    db.commit()

    clients = []

    for i in range(50):
        credit_score = random.randint(100, 1000)
        monthly_income = round(random.uniform(1500.0, 25000.0), 2)

        client = Client(
            name=fake.name(),
            cpf=generate_cpf(),
            email=fake.email(),
            monthly_income=monthly_income,
            credit_score=credit_score
        )
        db.add(client)
        db.flush()  # Gera o ID sem commitar

        # Gera entre 3 e 15 transações por cliente
        client_transactions = []
        for _ in range(random.randint(3, 15)):
            transaction = Transaction(
                client_id=client.id,
                amount=round(random.uniform(50.0, 5000.0), 2),
                transaction_type=random.choice(TRANSACTION_TYPES),
                merchant_category=random.choice(MERCHANT_CATEGORIES)
            )
            db.add(transaction)
            client_transactions.append(transaction)

        # Gera análise de risco para o cliente
        risk_level, risk_score, approved = calculate_risk(
            credit_score, monthly_income, client_transactions
        )

        analysis = CreditAnalysis(
            client_id=client.id,
            risk_level=risk_level,
            risk_score=round(risk_score, 4),
            approved=approved,
            analysis_notes=f"Análise automática — Score: {credit_score} | Renda: R${monthly_income}"
        )
        db.add(analysis)
        clients.append(client)

    db.commit()
    print(f"✅ {len(clients)} clientes criados com transações e análises de risco!")


if __name__ == "__main__":
    with Session(engine) as db:
        seed(db)