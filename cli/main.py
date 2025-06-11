import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from repositories.data_repository import DataRepository

from cli.controllers.customer_controller import (
    handle_add_customer,
    handle_list_customers,
    handle_edit_customer,
    handle_remove_customer
    )
from cli.controllers.plan_controller import (
    handle_add_plan,
    handle_list_plans,
    handle_edit_plan,
    handle_remove_plan
    )
from cli.controllers.contract_controller import (
    handle_create_contract,
    handle_list_contracts,
    handle_cancel_contract,
    handle_reactivate_contract,
    handle_remove_contract
)
from cli.controllers.invoice_controller import (
    handle_generate_invoice,
    handle_list_invoices,
    handle_pay_invoice,
    handle_remove_invoice
    )
from cli.controllers.ticket_controller import (
    handle_open_ticket,
    handle_list_tickets,
    handle_close_ticket,
    handle_reopen_ticket,
    handle_remove_ticket
)

DATA_FILE = "data.json"

def menu_principal() -> str:
    print("\n=== Sistema ISP ===")
    print("1. Clientes")
    print("2. Planos")
    print("3. Contratos")
    print("4. Faturas")
    print("5. Chamados")
    print("0. Sair")
    return input("Escolha o domínio: ").strip()

def submenu_clientes(customers, plans, contracts, invoices, tickets):
    while True:
        print("\n--- Clientes ---")
        print("1. Adicionar cliente")
        print("2. Listar clientes")
        print("3. Editar cliente")
        print("4. Remover cliente")
        print("0. Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            handle_add_customer(customers)
        elif op == "2":
            handle_list_customers(customers)
        elif op == "3":
            handle_edit_customer(customers)
        elif op == "4":
            handle_remove_customer(customers)
        elif op == "0":
            break
        else:
            print("> Opção inválida para Clientes.")

def submenu_planos(customers, plans, contracts, invoices, tickets):
    while True:
        print("\n--- Planos ---")
        print("1. Adicionar plano")
        print("2. Listar planos")
        print("3. Editar plano")
        print("4. Remover plano")
        print("0. Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            handle_add_plan(plans)
        elif op == "2":
            handle_list_plans(plans)
        elif op == "3":
            handle_edit_plan(plans)
        elif op == "4":
            handle_remove_plan(plans)
        elif op == "0":
            break
        else:
            print("> Opção inválida para Planos.")

def submenu_contratos(customers, plans, contracts, invoices, tickets):
    while True:
        print("\n--- Contratos ---")
        print("1. Criar contrato")
        print("2. Listar contratos")
        print("3. Cancelar contrato")
        print("4. Reativar contrato")
        print("5. Remover contrato")
        print("0. Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            handle_create_contract(customers, plans, contracts)
        elif op == "2":
            handle_list_contracts(contracts)
        elif op == "3":
            handle_cancel_contract(contracts)
        elif op == "4":
            handle_reactivate_contract(contracts)
        elif op == "5":
            handle_remove_contract(contracts)
        elif op == "0":
            break
        else:
            print("> Opção inválida para Contratos.")

def submenu_faturas(customers, plans, contracts, invoices, tickets):
    while True:
        print("\n--- Faturas ---")
        print("1. Gerar fatura")
        print("2. Listar faturas")
        print("3. Pagar fatura")
        print("4. Remover fatura")
        print("0. Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            handle_generate_invoice(contracts, invoices)
        elif op == "2":
            handle_list_invoices(invoices)
        elif op == "3":
            handle_pay_invoice(invoices)
        elif op == "4":
            handle_remove_invoice(invoices)
        elif op == "0":
            break
        else:
            print("> Opção inválida para Faturas.")

def submenu_chamados(customers, plans, contracts, invoices, tickets):
    while True:
        print("\n--- Chamados ---")
        print("1. Abrir chamado")
        print("2. Listar chamados")
        print("3. Fechar chamado")
        print("4. Reabrir chamado")
        print("5. Remover chamado")
        print("0. Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            handle_open_ticket(customers, tickets)
        elif op == "2":
            handle_list_tickets(tickets)
        elif op == "3":
            handle_close_ticket(tickets)
        elif op == "4":
            handle_reopen_ticket(tickets)
        elif op == "5":
            handle_remove_ticket(tickets)
        elif op == "0":
            break
        else:
            print("> Opção inválida para Chamados.")

def main():
    repo = DataRepository()
    customers, plans, contracts, invoices, tickets = repo.load()

    while True:
        dom = menu_principal()
        if dom == "1":
            submenu_clientes(customers, plans, contracts, invoices, tickets)
        elif dom == "2":
            submenu_planos(customers, plans, contracts, invoices, tickets)
        elif dom == "3":
            submenu_contratos(customers, plans, contracts, invoices, tickets)
        elif dom == "4":
            submenu_faturas(customers, plans, contracts, invoices, tickets)
        elif dom == "5":
            submenu_chamados(customers, plans, contracts, invoices, tickets)
        elif dom == "0":
            repo.save(customers, plans, contracts, invoices, tickets)
            print(f"> Dados salvos em {repo.filename}. Até logo!")
            break
        else:
            print("> Domínio inválido.")

if __name__ == "__main__":
    main()