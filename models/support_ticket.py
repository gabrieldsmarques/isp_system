# isp_system/models/support_ticket.py

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, ClassVar, Dict, Any
from models.customer import Customer
from exceptions import TicketAlreadyClosedError, TicketAlreadyOpenError

@dataclass
class SupportTicket:
    """
    Representa um chamado de suporte técnico para um cliente.
    """
    customer: Customer
    issue_description: str
    open_date: date

    # Campos internos inicializados no __post_init__
    id: int = field(init=False)
    status: str = field(init=False)
    close_date: Optional[date] = field(init=False)
    resolution: Optional[str] = field(init=False)

    # Contador de IDs como variável de classe
    _id_counter: ClassVar[int] = 0

    def __post_init__(self):
        # Gera um ID único incremental
        type(self)._id_counter += 1
        self.id = type(self)._id_counter
        self.status = "Aberto"
        self.close_date = None
        self.resolution = None

    def close(self, resolution: str, close_date: date) -> None:
        """
        Encerra o chamado com uma resolução e data de fechamento.
        """
        if self.status == "Fechado":
            raise TicketAlreadyClosedError(f"Chamado #{self.id} já está fechado.")
        self.status = "Fechado"
        self.resolution = resolution
        self.close_date = close_date

    def reopen(self, new_open_date: date) -> None:
        """
        Reabre um chamado já fechado, mantendo o histórico.
        """
        if self.status == "Aberto":
            raise TicketAlreadyOpenError(f"Chamado #{self.id} já está aberto.")
        self.status = "Aberto"
        self.open_date = new_open_date
        self.resolution = None
        self.close_date = None

    def get_status(self) -> str:
        """
        Retorna o status atual e datas importantes do chamado.
        """
        if self.status == "Aberto":
            return f"Aberto desde {self.open_date}"
        return f"Fechado em {self.close_date}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o chamado em um dicionário para persistência.
        """
        return {
            "id": self.id,
            "customer_cpf": self.customer.cpf,
            "issue_description": self.issue_description,
            "open_date": self.open_date.isoformat(),
            "status": self.status,
            "close_date": self.close_date.isoformat() if self.close_date else None,
            "resolution": self.resolution
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], cust_map: Dict[str, Customer]) -> SupportTicket:
        """
        Reconstrói um SupportTicket a partir do dicionário.
        """
        # Cria instância inicial (isso já incrementa o contador, mas vamos ajustar abaixo)
        tick = cls(
            customer=cust_map[data["customer_cpf"]],
            issue_description=data["issue_description"],
            open_date=date.fromisoformat(data["open_date"])
        )
        # Ajusta o ID e o contador conforme o salvo
        tick.id = data["id"]
        if data["id"] > cls._id_counter:
            cls._id_counter = data["id"]
        # Restaura status, datas e resolução
        tick.status = data["status"]
        tick.close_date = date.fromisoformat(data["close_date"]) if data["close_date"] else None
        tick.resolution = data["resolution"]
        return tick
