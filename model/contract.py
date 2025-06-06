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

    def __repr__(self) -> str:
        status = "Ativo" if self.active else "Inativo"
        return (
            f"<Contract customer={self.customer.name} "
            f"plan={self.plan.name} status={status}>"
        )
