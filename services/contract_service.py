from models.contract import Contract
from datetime import date
from typing import List

def create_contract(contracts: List[Contract], customer, plan, start_date: date) -> Contract:
    ctr = Contract(customer=customer, plan=plan, start_date=start_date)
    contracts.append(ctr)
    return ctr

def list_contracts(contracts: List[Contract]) -> List[str]:
    return [f"{c} | {c.get_status()}" for c in contracts]

def cancel_contract(contract: Contract, cancel_date: date) -> None:
    contract.cancel(cancel_date)

def reactivate_contract(contract: Contract, new_start_date: date) -> bool:
    if contract.active:
        return False
    contract.reactivate(new_start_date)
    return True

def remove_contract(contracts: List[Contract], index: int) -> Contract:
    return contracts.pop(index)
