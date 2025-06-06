class Customer:
    """
    Representa um cliente do ISP.
    """

    def __init__(self, ssn: str, name: str, address: str):
        """
        Inicializa um cliente com SSN, nome e endereço.

        :param ssn: SSN do cliente (string, sem formatação)
        :param name: Nome completo do cliente
        :param address: Endereço de instalação
        """
        self.ssn = ssn
        self.name = name
        self.address = address
        self.contract = None  # será vinculado quando um contrato for criado

    def attach_contract(self, contract) -> None:
        """
        Vincula o contrato ao cliente.

        :param contract: instância do contrato
        """
        self.contract = contract

    def get_status(self) -> str:
        """
        Retorna o status do cliente:
        - "Possui contrato" ou "Não possui contrato"

        :return: status atual do cliente
        """
        return "Possui contrato" if self.contract else "Não possui contrato"

    def __repr__(self) -> str:
        return f"<Customer ssn={self.ssn} name={self.name}>"
