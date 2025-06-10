import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import date, timedelta
from models.customer import Customer
from models.plan import Plan
from models.contract import Contract
from models.invoice import Invoice
from models.support_ticket import SupportTicket
from persistence.json_persistence import JsonPersistence
import re

DATA_FILE = "data.json"

def valid_ssn(ssn: str, existing_ssns: set) -> bool:
    """Valida SSN: 11 dígitos e não duplicado."""
    if not re.fullmatch(r"\d{11}", ssn):
        print("> SSN inválido: deve conter exatamente 11 dígitos numéricos.")
        return False
    if ssn in existing_ssns:
        print("> SSN já cadastrado.")
        return False
    return True

def valid_positive_number(value: str, field_name: str) -> float:
    """Converte string em float positivo."""
    try:
        num = float(value)
        if num <= 0:
            raise ValueError
        return num
    except ValueError:
        print(f"> Valor inválido para {field_name}: deve ser número positivo.")
        return None

def select_from_list(lst: list, label: str):
    """Helper: exibe lista enumerada e retorna índice escolhido ou None."""
    if not lst:
        print(f"> Nenhum {label} disponível.")
        return None
    for i, item in enumerate(lst, 1):
        print(f"{i}. {item}")
    try:
        idx = int(input(f"Índice do {label}: ").strip()) - 1
        if idx < 0 or idx >= len(lst):
            raise IndexError
        return idx
    except (ValueError, IndexError):
        print(f"> Índice inválido para {label}.")
        return None

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
        cust_map = {c.ssn: c for c in customers}
        plan_map = {p.name: p for p in plans}
        for raw_ctr in raw.get("contracts", []):
            ctr = Contract.from_dict(raw_ctr, cust_map, plan_map)
            contracts.append(ctr)

    # Reconstrução de faturas
    invoices = []
    if hasattr(Invoice, "from_dict"):
        ctr_map = {c.customer.ssn: c for c in contracts}
        for raw_inv in raw.get("invoices", []):
           inv = Invoice.from_dict(raw_inv, ctr_map)
           invoices.append(inv)

    # Reconstrução de chamados de suporte
    support_tickets = []
    if hasattr(SupportTicket, "from_dict"):
        cust_map = {c.ssn: c for c in customers}
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
            ssn = input("SSN (11 dígitos): ").strip()
            if not valid_ssn(ssn, {c.ssn for c in customers}):
                continue
            name = input("Nome: ").strip()
            address = input("Endereço: ").strip()
            customers.append(Customer(ssn=ssn, name=name, address=address))
            print("> Cliente adicionado.")

        elif choice == "2":
            if not customers: print("> Nenhum cliente cadastrado.")
            for c in customers:
                print(f" - {c} | {c.get_status()}")

        elif choice == "3":
            idx = select_from_list(customers, "cliente")
            if idx is None: continue
            c = customers[idx]
            new_name = input(f"Novo nome [{c.name}]: ").strip() or c.name
            new_address = input(f"Novo endereço [{c.address}]: ").strip() or c.address
            c.name, c.address = new_name, new_address
            print("> Cliente atualizado.")

        elif choice == "4":
            idx = select_from_list(customers, "cliente")
            if idx is None: continue
            removed = customers.pop(idx)
            print(f"> Cliente removido: {removed}")

        # Planos
        elif choice == "5":
            name = input("Nome do plano: ").strip()
            speed = valid_positive_number(input("Velocidade (Mbps): ").strip(), "velocidade")
            if speed is None: continue
            fee = valid_positive_number(input("Mensalidade: ").strip(), "mensalidade")
            if fee is None: continue
            plans.append(Plan(name=name, speed_mbps=speed, monthly_fee=fee))
            print("> Plano adicionado.")

        elif choice == "6":
            if not plans: print("> Nenhum plano cadastrado.")
            for p in plans:
                print(f" - {p} | {p.description()}")

        elif choice == "7":
            idx = select_from_list(plans, "plano")
            if idx is None: continue
            p = plans[idx]
            p.name = input(f"Novo nome [{p.name}]: ").strip() or p.name
            sp = input(f"Nova velocidade [{p.speed_mbps}]: ").strip()
            if sp:
                val = valid_positive_number(sp, "velocidade")
                if val is None: continue
                p.speed_mbps = val
            mf = input(f"Nova mensalidade [{p.monthly_fee}]: ").strip()
            if mf:
                val = valid_positive_number(mf, "mensalidade")
                if val is None: continue
                p.monthly_fee = val
            print("> Plano atualizado.")

        elif choice == "8":
            idx = select_from_list(plans, "plano")
            if idx is None: continue
            removed = plans.pop(idx)
            print(f"> Plano removido: {removed}")

        # Contratos
        elif choice == "9":
            if not customers or not plans:
                print("> É necessário ao menos um cliente e um plano.")
                continue
            ci = select_from_list(customers, "cliente")
            pi = select_from_list(plans, "plano")
            if ci is None or pi is None: continue
            contracts.append(Contract(
                customer=customers[ci],
                plan=plans[pi],
                start_date=date.today()
            ))
            print("> Contrato criado.")

        elif choice == "10":
            if not contracts: print("> Nenhum contrato.")
            for c in contracts:
                print(f" - {c} | {c.get_status()}")

        elif choice == "11":
            idx = select_from_list(contracts, "contrato")
            if idx is None: continue
            cont = contracts[idx]
            if not cont.active:
                print("> Contrato já está inativo.")
                continue
            cont.cancel(cancel_date=date.today())
            print("> Contrato cancelado.")

        elif choice == "12":
            idx = select_from_list(contracts, "contrato")
            if idx is None: continue
            cont = contracts[idx]
            if cont.active:
                print("> Contrato já ativo.")
                continue
            cont.reactivate(new_start_date=date.today())
            print("> Contrato reativado.")

        elif choice == "13":
            idx = select_from_list(contracts, "contrato")
            if idx is None: continue
            removed = contracts.pop(idx)
            print(f"> Contrato removido: {removed}")

        # Faturas
        elif choice == "14":
            ativos = [c for c in contracts if c.active]
            if not ativos:
                print("> Nenhum contrato ativo.")
                continue
            idx = select_from_list(ativos, "contrato ativo")
            if idx is None: continue
            invoices.append(Invoice(contract=ativos[idx], issue_date=date.today()))
            print("> Fatura gerada.")

        elif choice == "15":
            if not invoices: print("> Nenhuma fatura.")
            for i in invoices:
                print(f" - {i} | {i.get_status()}")

        elif choice == "16":
            idx = select_from_list(invoices, "fatura")
            if idx is None: continue
            inv = invoices[idx]
            if inv.paid:
                print("> Fatura já paga.")
                continue
            inv.pay(pay_date=date.today())
            print("> Fatura paga.")

        elif choice == "17":
            idx = select_from_list(invoices, "fatura")
            if idx is None: continue
            removed = invoices.pop(idx)
            print(f"> Fatura removida: {removed}")

        # Chamados
        elif choice == "18":
            ci = select_from_list(customers, "cliente")
            if ci is None: continue
            desc = input("Descrição do problema: ").strip()
            tickets.append(SupportTicket(
                customer=customers[ci],
                issue_description=desc,
                open_date=date.today()
            ))
            print("> Chamado aberto.")

        elif choice == "19":
            if not tickets: print("> Nenhum chamado.")
            for t in tickets:
                print(f" - {t} | {t.get_status()}")

        elif choice == "20":
            idx = select_from_list(tickets, "chamado")
            if idx is None: continue
            t = tickets[idx]
            if t.status == "Fechado":
                print("> Chamado já fechado.")
                continue
            resolution = input("Resolução: ").strip()
            t.close(resolution=resolution, close_date=date.today())
            print("> Chamado fechado.")

        elif choice == "21":
            idx = select_from_list(tickets, "chamado")
            if idx is None: continue
            t = tickets[idx]
            if t.status == "Aberto":
                print("> Chamado já aberto.")
                continue
            t.reopen(new_open_date=date.today())
            print("> Chamado reaberto.")

        elif choice == "22":
            idx = select_from_list(tickets, "chamado")
            if idx is None: continue
            removed = tickets.pop(idx)
            print(f"> Chamado removido: {removed}")

        elif choice == "0":
            save_data(customers, plans, contracts, invoices, tickets)
            print(f"> Dados salvos em {DATA_FILE}. Encerrando.")
            break

        else:
            print("> Opção inválida.")

if __name__ == "__main__":
    main()