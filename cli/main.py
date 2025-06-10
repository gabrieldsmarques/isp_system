import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import date, timedelta
from repositories.data_repository import DataRepository

from cli.utils import select_from_list
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


from models.customer import Customer

from models.plan import Plan
from models.contract import Contract
from models.invoice import Invoice
from models.support_ticket import SupportTicket

from validators.input_validators import valid_cpf, valid_positive_number

from services.customer_service import (
    add_customer,
    list_customers,
    update_customer,
    remove_customer
    )
from services.plan_service import (
    add_plan,
    list_plans,
    update_plan,
    remove_plan
    )
from services.contract_service import (
    create_contract,
    list_contracts,
    cancel_contract,
    reactivate_contract,
    remove_contract
    )
from services.invoice_service import (
    generate_invoice,
    list_invoices,
    pay_invoice,
    remove_invoice
    )
from services.support_ticket_service import (
    open_ticket,
    list_tickets,
    close_ticket, 
    reopen_ticket, 
    remove_ticket
    )

import re

DATA_FILE = "data.json"

def menu():
    print("\n=== Sistema ISP (CRUD + Validação) ===")
    print("1. Adicionar cliente")
    print("2. Listar clientes")
    print("3. Editar cliente")
    print("4. Remover cliente")
    print("5. Adicionar plano")
    print("6. Listar planos")
    print("7. Editar plano")
    print("8. Remover plano")
    print("9. Criar contrato")
    print("10. Listar contratos")
    print("11. Cancelar contrato")
    print("12. Reativar contrato")
    print("13. Remover contrato")
    print("14. Gerar fatura")
    print("15. Listar faturas")
    print("16. Pagar fatura")
    print("17. Remover fatura")
    print("18. Abrir chamado de suporte")
    print("19. Listar chamados")
    print("20. Fechar chamado")
    print("21. Reabrir chamado")
    print("22. Remover chamado")
    print("0. Sair")
    return input("Escolha uma opção: ").strip()


def main():
    repo = DataRepository() 
    customers, plans, contracts, invoices, tickets = repo.load()

    while True:
        choice = menu()

        # Clientes
        if choice == "1":
            handle_add_customer(customers)
        elif choice == "2":
            handle_list_customers(customers)
        elif choice == "3":
            handle_edit_customer(customers)
        elif choice == "4":
            handle_remove_customer(customers)

        # Planos
        elif choice == "5":
            handle_add_plan(plans)
        elif choice == "6":
            handle_list_plans(plans)
        elif choice == "7":
            handle_edit_plan(plans)
        elif choice == "8":
            handle_remove_plan(plans)

        # Contratos
        elif choice == "9":
            handle_create_contract(customers, plans, contracts)
        elif choice == "10":
            handle_list_contracts(contracts)
        elif choice == "11":
            handle_cancel_contract(contracts)
        elif choice == "12":
            handle_reactivate_contract(contracts)
        elif choice == "13":
            handle_remove_contract(contracts)

        # Faturas
        elif choice == "14":
            handle_generate_invoice(contracts, invoices)
        elif choice == "15":
            handle_list_invoices(invoices)
        elif choice == "16":
            handle_pay_invoice(invoices)
        elif choice == "17":
            handle_remove_invoice(invoices)

        # Chamados
        elif choice == "18":
            handle_open_ticket(customers, tickets)
        elif choice == "19":
            handle_list_tickets(tickets)
        elif choice == "20":
            handle_close_ticket(tickets)
        elif choice == "21":
            handle_reopen_ticket(tickets)
        elif choice == "22":
            handle_remove_ticket(tickets)

        # Sair
        elif choice == "0":
            repo.save(customers, plans, contracts, invoices, tickets)
            print(f"> Dados salvos em {repo.filename}. Encerrando.")
            break

        else:
            print("> Opção inválida.")

if __name__ == "__main__":
    main()