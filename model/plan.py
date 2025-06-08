class Plan:
    """
    Representa um plano de internet oferecido pelo ISP.
    """

    def __init__(self, name: str, speed_mbps: float, monthly_fee: float):
        """
        Inicializa um plano com nome, velocidade em Mbps e valor mensal.

        :param name: Nome do plano (ex: "Basic", "Premium")
        :param speed_mbps: Velocidade contratada em Mbps
        :param monthly_fee: Valor mensal em moeda local
        """
        self.name = name
        self.speed_mbps = speed_mbps
        self.monthly_fee = monthly_fee

    def description(self) -> str:
        """
        Retorna uma descrição breve do plano.

        :return: ex: "Plan Basic: 50.0 Mbps for $79.90/month"
        """
        return (f"Plan {self.name}: {self.speed_mbps:.1f} Mbps "
                f"for $ {self.monthly_fee:.2f}/month")

    def to_dict(self) -> dict:
        """
        Converte o plano em um dicionário para persistência.
        """
        return {
            "name": self.name,
            "speed_mbps": self.speed_mbps,
            "monthly_fee": self.monthly_fee
        }

    def __repr__(self) -> str:
        return f"<Plan name={self.name} {self.speed_mbps}Mbps ${self.monthly_fee:.2f}>"
