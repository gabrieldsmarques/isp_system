from cli.utils import select_from_list
from services.contract_service import (
    create_contract, list_contracts,
    cancel_contract, reactivate_contract, remove_contract
)
from models.contract import Contract
from datetime import date
from exceptions import ContractInactiveError, ContractActiveError

def handle_create_contract(customers: list, plans: list, contracts: list[Contract]) -> None:
    if not customers or not plans:
        print("> É necessário ao menos um cliente e um plano.")
        return
    ci = select_from_list(customers, "cliente")
    pi = select_from_list(plans, "plano")
    if ci is None or pi is None:
        return
    ctr = create_contract(contracts, customers[ci], plans[pi], date.today())
    print("> Contrato criado.")

def handle_list_contracts(contracts: list[Contract]) -> None:
    if not contracts:
        print("> Nenhum contrato.")
        return
    for desc in list_contracts(contracts):
        print(" - " + desc)

def handle_cancel_contract(contracts: list[Contract]) -> None:
    idx = select_from_list(contracts, "contrato")
    if idx is None:
        return
    try:
        cancel_contract(contracts[idx], date.today())
        print("> Contrato cancelado.")
    except ContractInactiveError as e:
        print(f"> {e}")

def handle_reactivate_contract(contracts: list[Contract]) -> None:
    idx = select_from_list(contracts, "contrato")
    if idx is None:
        return
    try:
        reactivate_contract(contracts[idx], date.today())
        print("> Contrato reativado.")
    except ContractActiveError as e:
        print(f"> {e}")

def handle_remove_contract(contracts: list[Contract]) -> None:
    idx = select_from_list(contracts, "contrato")
    if idx is None:
        return
    removed = remove_contract(contracts, idx)
    print(f"> Contrato removido: {removed}")
