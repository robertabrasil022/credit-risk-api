from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.connection import Base


# Enum para categorias de risco
class RiskLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    monthly_income = Column(Float, nullable=False)
    credit_score = Column(Integer, nullable=False)  # 0 a 1000
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento — um cliente tem muitas transações
    transactions = relationship("Transaction", back_populates="client")
    analyses = relationship("CreditAnalysis", back_populates="client")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(50), nullable=False)  # ex: compra, saque, transferencia
    merchant_category = Column(String(100))  # ex: alimentacao, viagem, eletronicos
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento — cada transação pertence a um cliente
    client = relationship("Client", back_populates="transactions")


class CreditAnalysis(Base):
    __tablename__ = "credit_analyses"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    risk_score = Column(Float, nullable=False)   # 0.0 a 1.0
    approved = Column(String(3), nullable=False)  # YES / NO
    analysis_notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento — cada análise pertence a um cliente
    client = relationship("Client", back_populates="analyses")