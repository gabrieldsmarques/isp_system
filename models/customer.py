class Customer:
    """
    Representa um cliente do ISP.
    """

    def __init__(self, cpf: str, name: str, address: str):
        """
        Inicializa um cliente com CPF, nome e endereço.

        :param cpf: CPF do cliente (string, sem formatação)
        :param name: Nome completo do cliente
        :param address: Endereço de instalação
        """
        self.cpf = cpf
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
    
    def to_dict(self) -> dict:
        """
        Converte o cliente em um dicionário para persistência.
        """
        return {
            "cpf": self.cpf,
            "name": self.name,
            "address": self.address
        }

    def __repr__(self) -> str:
        return f"<Customer cpf={self.cpf} name={self.name}>"
