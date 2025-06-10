from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Customer:
    """
    Representa um cliente do ISP.
    """
    cpf: str
    name: str
    address: str
    contract: Optional["Contract"] = None  

    def attach_contract(self, contract: "Contract") -> None:
        """
        Vincula o contrato ao cliente.
        """
        self.contract = contract

    def get_status(self) -> str:
        """
        Retorna o status do cliente:
        - "Possui contrato" ou "Não possui contrato"
        """
        return "Possui contrato" if self.contract else "Não possui contrato"

    def to_dict(self) -> dict:
        """
        Converte o cliente em um dicionário para persistência.
        """
        return {
            "cpf": self.cpf,
            "name": self.name,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data: dict) -> Customer:
        """
        Reconstrói um Customer a partir do dicionário.
        """
        return cls(
            cpf=data["cpf"],
            name=data["name"],
            address=data["address"]
        )
