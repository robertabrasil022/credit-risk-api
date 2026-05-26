from fastapi import FastAPI

# Inicializamos a aplicação FastAPI com metadados profissionais. 
# Recrutadores olham se você documenta o propósito do microsserviço.
app = FastAPI(
    title="Credit Risk Analysis Microservice",
    description="API interna para simulação e avaliação de risco de crédito de transações financeiras.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """
    Endpoint de Health Check (Checagem de Saúde).
    Útil para monitoramento em ambientes de nuvem (AWS/Azure) e clusters Kubernetes.
    """
    return {
        "status": "healthy",
        "service": "credit-risk-api",
        "version": "0.1.0"
    }