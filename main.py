from fastapi import FastAPI
from app.database.connection import engine, Base
from app.database import models
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Credit Risk Analysis Microservice",
    description="API interna para simulação e avaliação de risco de crédito de transações financeiras.",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "credit-risk-api",
        "version": "0.1.0"
    }