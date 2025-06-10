from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Plan:
    """
    Representa um plano de internet oferecido pelo ISP.
    """
    name: str
    speed_mbps: float
    monthly_fee: float

    def description(self) -> str:
        """
        Retorna uma descrição breve do plano.
        """
        return f"Plan {self.name}: {self.speed_mbps:.1f} Mbps for $ {self.monthly_fee:.2f}/month"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o plano em um dicionário para persistência.
        """
        return {
            "name": self.name,
            "speed_mbps": self.speed_mbps,
            "monthly_fee": self.monthly_fee
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Plan:
        """
        Reconstrói um Plan a partir do dicionário.
        """
        return cls(
            name=data["name"],
            speed_mbps=data["speed_mbps"],
            monthly_fee=data["monthly_fee"]
        )
