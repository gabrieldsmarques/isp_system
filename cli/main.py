import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import date, timedelta
from models.customer import Customer

from models.plan import Plan
from models.contract import Contract
from models.invoice import Invoice
from models.support_ticket import SupportTicket
from persistence.persistence import JsonPersistence
from validators.input_validators import valid_cpf, valid_positive_number
from cli.utils import select_from_list
from services.customer_service import (add_customer, list_customers, update_customer, remove_customer)
from services.plan_service import (add_plan, list_plans, update_plan, remove_plan)
from services.contract_service import (create_contract, list_contracts,cancel_contract, reactivate_contract, remove_contract)
from services.invoice_service import (generate_invoice, list_invoices,pay_invoice, remove_invoice)
from services.support_ticket_service import (open_ticket, list_tickets,close_ticket, reopen_ticket, remove_ticket)






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

def load_data(filename=DATA_FILE):
    """
    Carrega dados de JSON e reconstrói objetos via from_dict(),
    ou retorna listas vazias se o arquivo não existir.
    """
    try:
        raw = JsonPersistence.load(filename)
    except FileNotFoundError:
        return [], [], [], [], []

    # Reconstrução de clientes
    customers = []
    if hasattr(Customer, "from_dict"):
        for raw_cust in raw.get("customers", []):
            cust = Customer.from_dict(raw_cust)
            customers.append(cust)

    # Reconstrução de planos
    plans = []
    if hasattr(Plan, "from_dict"):
       for raw_plan in raw.get("plans", []):
            plan = Plan.from_dict(raw_plan)
            plans.append(plan)

    # Reconstrução de contratos
    contracts = []
    if hasattr(Contract, "from_dict"):
        cust_map = {c.cpf: c for c in customers}
        plan_map = {p.name: p for p in plans}
        for raw_ctr in raw.get("contracts", []):
            ctr = Contract.from_dict(raw_ctr, cust_map, plan_map)
            contracts.append(ctr)

    # Reconstrução de faturas
    invoices = []
    if hasattr(Invoice, "from_dict"):
        ctr_map = {c.customer.cpf: c for c in contracts}
        for raw_inv in raw.get("invoices", []):
           inv = Invoice.from_dict(raw_inv, ctr_map)
           invoices.append(inv)

    # Reconstrução de chamados de suporte
    support_tickets = []
    if hasattr(SupportTicket, "from_dict"):
        cust_map = {c.cpf: c for c in customers}
        for raw_tick in raw.get("support_tickets", []):
            tick = SupportTicket.from_dict(raw_tick, cust_map)
            support_tickets.append(tick)

    return customers, plans, contracts, invoices, support_tickets

def save_data(customers, plans, contracts, invoices, tickets):
    data = {
        "customers": [c.to_dict() for c in customers],
        "plans": [p.to_dict() for p in plans],
        "contracts": [c.to_dict() for c in contracts],
        "invoices": [i.to_dict() for i in invoices],
        "support_tickets": [t.to_dict() for t in tickets],
    }
    JsonPersistence.save(DATA_FILE, data)

def main():
    customers, plans, contracts, invoices, tickets = load_data()

    while True:
        choice = menu()

        # Clientes
        if choice == "1":
            cpf = input("CPF (11 dígitos): ").strip()
            name = input("Nome: ").strip()
            address = input("Endereço: ").strip()
            new = add_customer(customers, cpf, name, address)
            if new:
                print("> Cliente adicionado.")
                
        elif choice == "2":
            for desc in list_customers(customers):
                print(" - " + desc)
                
        elif choice == "3":
            idx = select_from_list(customers, "cliente")
            if idx is not None:
                c = customers[idx]
                new_name = input(f"Novo nome [{c.name}]: ").strip() or c.name
                new_address = input(f"Novo endereço [{c.address}]: ").strip() or c.address
                update_customer(c, new_name, new_address)
                print("> Cliente atualizado.")
                
        elif choice == "4":
            idx = select_from_list(customers, "cliente")
            if idx is not None:
                removed = remove_customer(customers, idx)
                print(f"> Cliente removido: {removed}")
                
        # Planos (5–8)
        elif choice == "5":
            name = input("Nome do plano: ").strip()
            speed_str = input("Velocidade (Mbps): ").strip()
            fee_str = input("Mensalidade: ").strip()
            new = add_plan(plans, name, speed_str, fee_str)
            if new:
                print("> Plano adicionado.")

        elif choice == "6":
            for desc in list_plans(plans):
                print(" - " + desc)

        elif choice == "7":
            idx = select_from_list(plans, "plano")
            if idx is not None:
                p = plans[idx]
                new_name = input(f"Novo nome [{p.name}]: ").strip()
                speed_str = input(f"Nova velocidade [{p.speed_mbps}]: ").strip()
                fee_str = input(f"Nova mensalidade [{p.monthly_fee}]: ").strip()
                ok = update_plan(p, new_name, speed_str, fee_str)
                if ok:
                    print("> Plano atualizado.")

        elif choice == "8":
            idx = select_from_list(plans, "plano")
            if idx is not None:
                removed = remove_plan(plans, idx)
                print(f"> Plano removido: {removed}")


        # Contratos (9–13)
        elif choice == "9":
            if not customers or not plans:
                print("> É necessário ao menos um cliente e um plano.")
            else:
                ci = select_from_list(customers, "cliente")
                pi = select_from_list(plans, "plano")
                if ci is not None and pi is not None:
                    from datetime import date
                    ctr = create_contract(contracts, customers[ci], plans[pi], date.today())
                    print("> Contrato criado.")

        elif choice == "10":
            for desc in list_contracts(contracts):
                print(" - " + desc)

        elif choice == "11":
            idx = select_from_list(contracts, "contrato")
            if idx is not None:
                from datetime import date
                ok = cancel_contract(contracts[idx], date.today())
                if ok:
                    print("> Contrato cancelado.")
                else:
                    print("> Contrato já está inativo.")

        elif choice == "12":
            idx = select_from_list(contracts, "contrato")
            if idx is not None:
                from datetime import date
                ok = reactivate_contract(contracts[idx], date.today())
                if ok:
                    print("> Contrato reativado.")
                else:
                    print("> Contrato já está ativo.")

        elif choice == "13":
            idx = select_from_list(contracts, "contrato")
            if idx is not None:
                removed = remove_contract(contracts, idx)
                print(f"> Contrato removido: {removed}")


        # Faturas (14–17)
        elif choice == "14":
            ativos = [c for c in contracts if c.active]
            if not ativos:
                print("> Nenhum contrato ativo.")
            else:
                idx = select_from_list(ativos, "contrato ativo")
                if idx is not None:
                    from datetime import date
                    inv = generate_invoice(invoices, ativos[idx], date.today())
                    print("> Fatura gerada.")

        elif choice == "15":
            for desc in list_invoices(invoices):
                print(" - " + desc)

        elif choice == "16":
            idx = select_from_list(invoices, "fatura")
            if idx is not None:
                from datetime import date
                ok = pay_invoice(invoices[idx], date.today())
                if ok:
                    print("> Fatura paga.")
                else:
                    print("> Fatura já paga.")

        elif choice == "17":
            idx = select_from_list(invoices, "fatura")
            if idx is not None:
                removed = remove_invoice(invoices, idx)
                print(f"> Fatura removida: {removed}")


        # Chamados (18–22)
        elif choice == "18":
            ci = select_from_list(customers, "cliente")
            if ci is not None:
                desc = input("Descrição do problema: ").strip()
                from datetime import date
                tick = open_ticket(tickets, customers[ci], desc, date.today())
                print("> Chamado aberto.")

        elif choice == "19":
            for desc in list_tickets(tickets):
                print(" - " + desc)

        elif choice == "20":
            idx = select_from_list(tickets, "chamado")
            if idx is not None:
                res = input("Resolução: ").strip()
                from datetime import date
                ok = close_ticket(tickets[idx], res, date.today())
                if ok:
                    print("> Chamado fechado.")
                else:
                    print("> Chamado já está fechado.")

        elif choice == "21":
            idx = select_from_list(tickets, "chamado")
            if idx is not None:
                from datetime import date
                ok = reopen_ticket(tickets[idx], date.today())
                if ok:
                    print("> Chamado reaberto.")
                else:
                    print("> Chamado já está aberto.")

        elif choice == "22":
            idx = select_from_list(tickets, "chamado")
            if idx is not None:
                removed = remove_ticket(tickets, idx)
                print(f"> Chamado removido: {removed}")

        elif choice == "0":
            save_data(customers, plans, contracts, invoices, tickets)
            print(f"> Dados salvos em {DATA_FILE}. Encerrando.")
            break

        else:
            print("> Opção inválida.")

if __name__ == "__main__":
    main()