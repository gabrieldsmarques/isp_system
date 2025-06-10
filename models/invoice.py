from datetime import date, timedelta

class Invoice:
    """
    Representa uma fatura mensal gerada para um contrato.
    """

    def __init__(self, contract, issue_date: date):
        """
        Inicializa uma fatura para o contrato informado.

        :param contract: instância de Contract
        :param issue_date: data de emissão da fatura
        """
        self.contract = contract
        self.issue_date = issue_date
        self.amount = contract.plan.monthly_fee
        # vencimento em 30 dias após a emissão
        self.due_date = issue_date + timedelta(days=30)
        self.paid = False
        self.paid_date = None

    def pay(self, pay_date: date) -> None:
        """
        Registra pagamento da fatura em determinada data.

        :param pay_date: data do pagamento
        """
        if self.paid:
            print("Fatura já foi paga.")
            return
        self.paid = True
        self.paid_date = pay_date

    def get_status(self) -> str:
        """
        Retorna o status da fatura:
        - "Pago em YYYY-MM-DD" ou "Aberta (vencimento em YYYY-MM-DD)"

        :return: status da fatura
        """
        if self.paid:
            return f"Pago em {self.paid_date}"
        return f"Aberta (vencimento em {self.due_date})"

    def to_dict(self) -> dict:
        """
        Converte a fatura em um dicionário para persistência.
        """
        return {
            "customer_ssn": self.contract.customer.ssn,
            "issue_date": self.issue_date.isoformat(),
            "amount": self.amount,
            "due_date": self.due_date.isoformat(),
            "paid": self.paid,
            "paid_date": self.paid_date.isoformat() if self.paid_date else None
        }
        
    def __repr__(self) -> str:
        status = "Pago" if self.paid else "Aberta"
        return (
            f"<Invoice customer={self.contract.customer.name} "
            f"amount={self.amount:.2f} status={status}>"
        )
