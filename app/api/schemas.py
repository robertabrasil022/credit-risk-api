from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.database.models import RiskLevel


# Schema de uma transação retornada pela API
class TransactionResponse(BaseModel):
    id: int
    amount: float
    transaction_type: str
    merchant_category: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# Schema resumido do cliente (usado em listagens)
class ClientSummary(BaseModel):
    id: int
    name: str
    credit_score: int
    monthly_income: float

    model_config = {"from_attributes": True}


# Schema completo do cliente (usado na busca por ID)
class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    credit_score: int
    monthly_income: float
    created_at: datetime
    transactions: list[TransactionResponse] = []

    model_config = {"from_attributes": True}


# Schema da análise de risco
class CreditAnalysisResponse(BaseModel):
    id: int
    risk_level: RiskLevel
    risk_score: float
    approved: str
    analysis_notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# Schema da resposta completa — cliente + análise
class ClientAnalysisResponse(BaseModel):
    client: ClientSummary
    analysis: CreditAnalysisResponse

    model_config = {"from_attributes": True}