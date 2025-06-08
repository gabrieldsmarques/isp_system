from datetime import date


class SupportTicket:
    """
    Representa um chamado de suporte técnico para um cliente.
    """

    _id_counter = 0  # contador de IDs

    def __init__(self, customer, issue_description: str, open_date: date):
        """
        Inicializa um chamado de suporte.

        :param customer: instância de Customer
        :param issue_description: descrição do problema relatado
        :param open_date: data de abertura do chamado
        """
        
        type(self)._id_counter += 1 # incrementa o contador e atribui o ID
        self.id = type(self)._id_counter
        self.customer = customer
        self.issue_description = issue_description
        self.open_date = open_date
        self.status = "Aberto"
        self.close_date = None
        self.resolution = None

    def close(self, resolution: str, close_date: date) -> None:
        """
        Encerra o chamado com uma resolução e data de fechamento.

        :param resolution: descrição de como o problema foi resolvido
        :param close_date: data de encerramento do chamado
        """
        if self.status == "Fechado":
            print(f"Chamado #{self.id} já está fechado.")
            return
        self.status = "Fechado"
        self.resolution = resolution
        self.close_date = close_date

    def reopen(self, new_open_date: date) -> None:
        """
        Reabre um chamado já fechado, mantendo o histórico.

        :param new_open_date: nova data de abertura
        """
        if self.status == "Aberto":
            print(f"Chamado #{self.id} já está aberto.")
            return
        self.status = "Aberto"
        self.open_date = new_open_date
        self.resolution = None
        self.close_date = None

    def get_status(self) -> str:
        """
        Retorna o status atual e datas importantes do chamado.

        :return: ex: "Aberto desde 2025-06-08" ou "Fechado em 2025-06-09"
        """
        if self.status == "Aberto":
            return f"Aberto desde {self.open_date}"
        return f"Fechado em {self.close_date}"

    def __repr__(self) -> str:
        return (
            f"<SupportTicket #{self.id} customer={self.customer.name} "
            f"status={self.status}>"
        )
