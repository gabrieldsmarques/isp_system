from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any
from exceptions import ContractInactiveError, ContractActiveError
from models.customer import Customer
from models.plan import Plan


@dataclass
class Contract:
    """
    Representa um contrato entre um cliente e um plano.
    """
    customer: Customer
    plan: Plan
    start_date: date
    active: bool = True
    end_date: Optional[date] = None

    def __post_init__(self):
        # Vincula automaticamente ao cliente
        self.customer.attach_contract(self)

    def cancel(self, cancel_date: date) -> None:
        """
        Cancela o contrato em determinada data.
        """
        if not self.active:
            raise ContractInactiveError("Contrato já está inativo.")
        self.active = False
        self.end_date = cancel_date

    def reactivate(self, new_start_date: date) -> None:
        """
        Reativa um contrato cancelado, iniciando novo ciclo.
        """
        if self.active:
            raise ContractActiveError("Contrato já está ativo.")
        self.active = True
        self.start_date = new_start_date
        self.end_date = None

    def get_status(self) -> str:
        """
        Retorna o status atual do contrato.
        """
        return "Ativo" if self.active else f"Inativo (encerrado em {self.end_date})"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o contrato em um dicionário para persistência.
        """
        return {
            "customer_cpf": self.customer.cpf,
            "plan_name": self.plan.name,
            "start_date": self.start_date.isoformat(),
            "active": self.active,
            "end_date": self.end_date.isoformat() if self.end_date else None
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        cust_map: Dict[str, Customer],
        plan_map: Dict[str, Plan]
    ) -> Contract:
        """
        Reconstrói um Contract a partir do dicionário.
        """
        start = date.fromisoformat(data["start_date"])
        ctr = cls(
            customer=cust_map[data["customer_cpf"]],
            plan=plan_map[data["plan_name"]],
            start_date=start
        )
        ctr.active = data["active"]
        if data["end_date"] is not None:
            ctr.end_date = date.fromisoformat(data["end_date"])
        return ctr
