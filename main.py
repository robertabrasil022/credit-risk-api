from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import HTMLResponse
from app.database.connection import engine, Base
from app.database import models
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Credit Risk Analysis Microservice",
    description="API interna para simulação e avaliação de risco de crédito de transações financeiras.",
    version="0.1.0",
    docs_url="/docs",     
    redoc_url="/redoc"     
)

app.include_router(router)

@app.get("/", response_model=dict)
def read_root():
    return {
        "status": "healthy",
        "service": "credit-risk-api",
        "version": "0.1.0"
    }