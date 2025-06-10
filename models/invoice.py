from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional, Dict, Any
from models.contract import Contract
from exceptions import InvoiceAlreadyPaidError

@dataclass
class Invoice:
    """
    Representa uma fatura mensal gerada para um contrato.
    """
    contract: Contract
    issue_date: date
    amount: float = field(init=False)
    due_date: date = field(init=False)
    paid: bool = False
    paid_date: Optional[date] = None

    def __post_init__(self):
        # Define amount e due_date automaticamente
        self.amount = self.contract.plan.monthly_fee
        self.due_date = self.issue_date + timedelta(days=30)

    def pay(self, pay_date: date) -> None:
        """
        Registra pagamento da fatura em determinada data.
        """
        if self.paid:
            raise InvoiceAlreadyPaidError("Fatura já foi paga.")
        self.paid = True
        self.paid_date = pay_date

    def get_status(self) -> str:
        """
        Retorna o status da fatura.
        """
        if self.paid:
            return f"Pago em {self.paid_date}"
        return f"Aberta (vencimento em {self.due_date})"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a fatura em um dicionário para persistência.
        """
        return {
            "customer_cpf": self.contract.customer.cpf,
            "issue_date": self.issue_date.isoformat(),
            "amount": self.amount,
            "due_date": self.due_date.isoformat(),
            "paid": self.paid,
            "paid_date": self.paid_date.isoformat() if self.paid_date else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], ctr_map: Dict[str, Contract]) -> Invoice:
        """
        Reconstrói um Invoice a partir do dicionário.
        """
        issue = date.fromisoformat(data["issue_date"])
        inv = cls(
            contract=ctr_map[data["customer_cpf"]],
            issue_date=issue
        )
        # restaurar estado
        inv.amount = data["amount"]
        inv.due_date = date.fromisoformat(data["due_date"])
        inv.paid = data["paid"]
        if data["paid_date"]:
            inv.paid_date = date.fromisoformat(data["paid_date"])
        return inv
