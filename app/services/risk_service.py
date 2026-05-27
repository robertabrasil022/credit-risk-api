from app.database.models import RiskLevel


class RiskAnalysisService:
    """
    Serviço de análise de risco de crédito.
    Responsável por calcular o score de risco baseado
    em dados financeiros do cliente.
    """

    # Pesos de cada fator na composição do risco
    WEIGHT_SCORE = 0.50
    WEIGHT_INCOME = 0.30
    WEIGHT_TRANSACTIONS = 0.20

    # Referências para normalização
    MAX_CREDIT_SCORE = 1000
    MAX_INCOME = 20000.0
    MAX_TRANSACTIONS = 20

    def calculate_risk(
        self,
        credit_score: int,
        monthly_income: float,
        total_transactions: int,
        total_transaction_amount: float
    ) -> dict:
        """
        Calcula o risco de crédito de um cliente.

        Args:
            credit_score: Score de crédito (0 a 1000)
            monthly_income: Renda mensal em reais
            total_transactions: Quantidade de transações
            total_transaction_amount: Soma total das transações

        Returns:
            Dicionário com risk_level, risk_score e approved
        """

        # Normaliza cada fator para 0.0 a 1.0
        score_factor = credit_score / self.MAX_CREDIT_SCORE
        income_factor = min(monthly_income / self.MAX_INCOME, 1.0)
        transaction_factor = min(total_transactions / self.MAX_TRANSACTIONS, 1.0)

        # Calcula o score final ponderado
        risk_score = (
            (score_factor * self.WEIGHT_SCORE) +
            (income_factor * self.WEIGHT_INCOME) +
            (transaction_factor * self.WEIGHT_TRANSACTIONS)
        )

        # Fator de endividamento — penaliza quem gasta muito em relação à renda
        if monthly_income > 0:
            debt_ratio = min(total_transaction_amount / (monthly_income * 3), 1.0)
            risk_score = risk_score * (1 - (debt_ratio * 0.2))

        risk_score = round(risk_score, 4)

        # Classifica o nível de risco
        if risk_score >= 0.75:
            risk_level = RiskLevel.LOW
            approved = "YES"
            notes = f"Perfil de baixo risco. Score sólido e renda compatível."
        elif risk_score >= 0.50:
            risk_level = RiskLevel.MEDIUM
            approved = "YES"
            notes = f"Perfil de risco moderado. Aprovado com reservas."
        elif risk_score >= 0.25:
            risk_level = RiskLevel.HIGH
            approved = "NO"
            notes = f"Perfil de alto risco. Renda ou score insuficientes."
        else:
            risk_level = RiskLevel.CRITICAL
            approved = "NO"
            notes = f"Perfil crítico. Crédito negado por alto risco de inadimplência."

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "approved": approved,
            "analysis_notes": f"{notes} | Score: {credit_score} | Renda: R${monthly_income:.2f}"
        }


# Instância global do serviço
risk_service = RiskAnalysisService()