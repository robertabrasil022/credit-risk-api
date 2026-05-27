from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Client, CreditAnalysis
from app.api.schemas import (
    ClientSummary,
    ClientResponse,
    ClientAnalysisResponse,
)

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientSummary])
def list_clients(db: Session = Depends(get_db)):
    """Retorna lista resumida de todos os clientes."""
    clients = db.query(Client).all()
    return clients


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Retorna dados completos de um cliente com suas transações."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.get("/{client_id}/analysis", response_model=ClientAnalysisResponse)
def get_client_analysis(client_id: int, db: Session = Depends(get_db)):
    """Retorna a análise de risco de crédito de um cliente."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    analysis = db.query(CreditAnalysis).filter(
        CreditAnalysis.client_id == client_id
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Análise não encontrada")

    return {"client": client, "analysis": analysis}