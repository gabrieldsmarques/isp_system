from typing import List
from datetime import date
from models.contract import Contract
from exceptions import ContractInactiveError, ContractActiveError

def create_contract(contracts: List[Contract], customer, plan, start_date: date) -> Contract:
    ctr = Contract(customer=customer, plan=plan, start_date=start_date)
    contracts.append(ctr)
    return ctr

def list_contracts(contracts: List[Contract]) -> list[str]:
    return [f"{c} | {c.get_status()}" for c in contracts]

def cancel_contract(contract: Contract, cancel_date: date) -> bool:
    """
    Retorna True se cancelou com sucesso, False se já estava inativo.
    """
    try:
        contract.cancel(cancel_date)
        return True
    except ContractInactiveError:
        return False

def reactivate_contract(contract: Contract, new_start_date: date) -> bool:
    """
    Retorna True se reativou com sucesso, False se já estava ativo.
    """
    try:
        contract.reactivate(new_start_date)
        return True
    except ContractActiveError:
        return False

def remove_contract(contracts: List[Contract], index: int) -> Contract:
    return contracts.pop(index)
