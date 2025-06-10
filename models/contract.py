from datetime import date

class Contract:
    """
    Representa um contrato entre um cliente e um plano.
    """

    def __init__(self, customer, plan, start_date: date):
        """
        Inicializa um contrato vinculando um Customer a um Plan.

        :param customer: instância de Customer
        :param plan: instância de Plan
        :param start_date: data de início do contrato
        """
        self.customer = customer
        self.plan = plan
        self.start_date = start_date
        self.active = True
        self.end_date = None

        # Ao criar, anexa ao cliente
        customer.attach_contract(self)

    def cancel(self, cancel_date: date) -> None:
        """
        Cancela o contrato em determinada data.

        :param cancel_date: data de cancelamento
        """
        if not self.active:
            print("Contrato já está inativo.")
            return
        self.active = False
        self.end_date = cancel_date

    def reactivate(self, new_start_date: date) -> None:
        """
        Reativa um contrato cancelado, iniciando novo ciclo.

        :param new_start_date: nova data de início
        """
        if self.active:
            print("Contrato já está ativo.")
            return
        self.active = True
        self.start_date = new_start_date
        self.end_date = None

    def get_status(self) -> str:
        """
        Retorna o status atual do contrato:
        - "Ativo" ou "Inativo (encerrado em YYYY-MM-DD)"

        :return: status do contrato
        """
        return "Ativo" if self.active else f"Inativo (encerrado em {self.end_date})"

    def to_dict(self) -> dict:
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
    def from_dict(cls, data: dict, cust_map: dict, plan_map: dict) -> "Contract":
        start = date.fromisoformat(data["start_date"])
        ctr = cls(
            customer=cust_map[data["customer_cpf"]],
            plan=plan_map[data["plan_name"]],
            start_date=start
        )
        # restaurar estado
        ctr.active = data["active"]
        if data["end_date"] is not None:
            ctr.end_date = date.fromisoformat(data["end_date"])
        return ctr
        
    def __repr__(self) -> str:
        status = "Ativo" if self.active else "Inativo"
        return (
            f"<Contract customer={self.customer.name} "
            f"plan={self.plan.name} status={status}>"
        )
