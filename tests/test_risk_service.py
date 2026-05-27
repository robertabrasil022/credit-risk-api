import pytest
from app.services.risk_service import RiskAnalysisService
from app.database.models import RiskLevel

# Instância do serviço para os testes
service = RiskAnalysisService()


class TestRiskAnalysisService:
    """Testes unitários para o serviço de análise de risco."""

    def test_low_risk_profile(self):
        """Cliente com score alto e renda alta deve ter risco LOW."""
        result = service.calculate_risk(
            credit_score=950,
            monthly_income=15000.0,
            total_transactions=10,
            total_transaction_amount=2000.0
        )
        assert result["risk_level"] == RiskLevel.LOW
        assert result["approved"] == "YES"
        assert result["risk_score"] >= 0.75

    def test_critical_risk_profile(self):
        """Cliente com score baixo e renda baixa deve ter risco CRITICAL."""
        result = service.calculate_risk(
            credit_score=100,
            monthly_income=1500.0,
            total_transactions=2,
            total_transaction_amount=8000.0
        )
        assert result["risk_level"] == RiskLevel.CRITICAL
        assert result["approved"] == "NO"
        assert result["risk_score"] < 0.25

    def test_approved_yes_for_low_risk(self):
        """Risco LOW deve sempre resultar em aprovação."""
        result = service.calculate_risk(
            credit_score=900,
            monthly_income=12000.0,
            total_transactions=15,
            total_transaction_amount=1500.0
        )
        assert result["approved"] == "YES"

    def test_approved_no_for_high_risk(self):
        """Risco HIGH deve sempre resultar em reprovação."""
        result = service.calculate_risk(
            credit_score=200,
            monthly_income=1800.0,
            total_transactions=3,
            total_transaction_amount=500.0
        )
        assert result["approved"] == "NO"

    def test_risk_score_between_zero_and_one(self):
        """Risk score deve sempre estar entre 0.0 e 1.0."""
        result = service.calculate_risk(
            credit_score=500,
            monthly_income=5000.0,
            total_transactions=8,
            total_transaction_amount=2000.0
        )
        assert 0.0 <= result["risk_score"] <= 1.0

    def test_analysis_notes_not_empty(self):
        """Análise deve sempre retornar uma nota explicativa."""
        result = service.calculate_risk(
            credit_score=600,
            monthly_income=6000.0,
            total_transactions=5,
            total_transaction_amount=1000.0
        )
        assert result["analysis_notes"] is not None
        assert len(result["analysis_notes"]) > 0

    def test_debt_ratio_penalizes_high_spending(self):
        """Alto volume de gastos em relação à renda deve reduzir o score."""
        result_low_debt = service.calculate_risk(
            credit_score=700,
            monthly_income=8000.0,
            total_transactions=10,
            total_transaction_amount=1000.0
        )
        result_high_debt = service.calculate_risk(
            credit_score=700,
            monthly_income=8000.0,
            total_transactions=10,
            total_transaction_amount=20000.0
        )
        assert result_low_debt["risk_score"] > result_high_debt["risk_score"]