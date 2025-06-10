from models.customer import Customer
from validators.input_validators import valid_cpf
from typing import List, Optional

def add_customer(customers: List[Customer], cpf: str, name: str, address: str) -> Optional[Customer]:
    """
    Tenta criar um Customer; retorna a instância se válido, ou None caso contrário.
    """
    if not valid_cpf(cpf, {c.cpf for c in customers}):
        return None
    cust = Customer(cpf=cpf, name=name, address=address)
    customers.append(cust)
    return cust

def list_customers(customers: List[Customer]) -> List[str]:
    """
    Retorna uma lista de strings descritivas para exibição.
    """
    return [f"{c} | {c.get_status()}" for c in customers]

def update_customer(customer: Customer, new_name: str, new_address: str) -> None:
    """
    Atualiza nome e endereço de um cliente já existente.
    """
    customer.name = new_name
    customer.address = new_address

def remove_customer(customers: List[Customer], index: int) -> Customer:
    """
    Remove e retorna o cliente no índice informado.
    """
    return customers.pop(index)
