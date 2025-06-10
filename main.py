from datetime import date, timedelta
from model.customer import Customer
from model.plan import Plan
from model.contract import Contract
from model.invoice import Invoice
from model.support_ticket import SupportTicket
from persistence import JsonPersistence

# Arquivo padrão de persistência
DATA_FILE = "data.json"

def menu():
    print("\n=== Sistema ISP ===")
    print("1. Adicionar cliente")
    print("2. Listar clientes")
    print("3. Adicionar plano")
    print("4. Listar planos")
    print("5. Criar contrato")
    print("6. Listar contratos")
    print("7. Gerar fatura")
    print("8. Listar faturas")
    print("9. Abrir chamado de suporte")
    print("10. Listar chamados")
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

    # Reconstrução usando métodos from_dict(), se disponíveis
    if hasattr(Customer, "from_dict"):
        customers = [Customer.from_dict(d) for d in raw.get("customers", [])]
    else:
        customers = []

    if hasattr(Plan, "from_dict"):
        plans = [Plan.from_dict(d) for d in raw.get("plans", [])]
    else:
        plans = []

    if hasattr(Contract, "from_dict"):
        contracts = [
            Contract.from_dict(d,
                               {c.ssn: c for c in customers},
                               {p.name: p for p in plans})
            for d in raw.get("contracts", [])
        ]
    else:
        contracts = []

    if hasattr(Invoice, "from_dict"):
        invoices = [
            Invoice.from_dict(d,
                              {ctr.customer.ssn: ctr for ctr in contracts})
            for d in raw.get("invoices", [])
        ]
    else:
        invoices = []

    if hasattr(SupportTicket, "from_dict"):
        support_tickets = [
            SupportTicket.from_dict(d,
                                    {c.ssn: c for c in customers})
            for d in raw.get("support_tickets", [])
        ]
    else:
        support_tickets = []

    return customers, plans, contracts, invoices, support_tickets

def save_data(customers, plans, contracts, invoices, tickets, filename=DATA_FILE):
    """
    Salva todos os dados em um arquivo JSON.
    """
    data = {
        "customers": [c.to_dict() for c in customers],
        "plans": [p.to_dict() for p in plans],
        "contracts": [c.to_dict() for c in contracts],
        "invoices": [i.to_dict() for i in invoices],
        "support_tickets": [t.to_dict() for t in tickets],
    }
    JsonPersistence.save(filename, data)

def main():
    # auto-load de dados
    customers, plans, contracts, invoices, tickets = load_data()

    while True:
        choice = menu()

        if choice == "1":
            ssn = input("SSN: ")
            name = input("Nome: ")
            address = input("Endereço: ")
            c = Customer(ssn=ssn, name=name, address=address)
            customers.append(c)
            print(f"> Cliente adicionado: {c}")

        elif choice == "2":
            if not customers:
                print("> Nenhum cliente cadastrado.")
            for c in customers:
                print(f"  - {c} | {c.get_status()}")

        elif choice == "3":
            name = input("Nome do plano: ")
            speed = float(input("Velocidade (Mbps): "))
            fee = float(input("Mensalidade: "))
            p = Plan(name=name, speed_mbps=speed, monthly_fee=fee)
            plans.append(p)
            print(f"> Plano adicionado: {p}")

        elif choice == "4":
            if not plans:
                print("> Nenhum plano cadastrado.")
            for p in plans:
                print(f"  - {p} | {p.description()}")

        elif choice == "5":
            if not customers or not plans:
                print("> É necessário ao menos um cliente e um plano.")
                continue
            print("Selecione cliente por índice:")
            for i, c in enumerate(customers, 1):
                print(f"{i}. {c.name}")
            ci = int(input("Índice do cliente: ")) - 1

            print("Selecione plano por índice:")
            for i, p in enumerate(plans, 1):
                print(f"{i}. {p.name}")
            pi = int(input("Índice do plano: ")) - 1

            ctr = Contract(
                customer=customers[ci],
                plan=plans[pi],
                start_date=date.today()
            )
            contracts.append(ctr)
            print(f"> Contrato criado: {ctr}")

        elif choice == "6":
            if not contracts:
                print("> Nenhum contrato criado.")
            for ctr in contracts:
                print(f"  - {ctr} | {ctr.get_status()}")

        elif choice == "7":
            ativos = [c for c in contracts if c.active]
            if not ativos:
                print("> É necessário ao menos um contrato ativo.")
                continue
            print("Selecione contrato para faturar:")
            for i, c in enumerate(ativos, 1):
                print(f"{i}. {c}")
            ci = int(input("Índice do contrato: ")) - 1

            inv = Invoice(contract=ativos[ci], issue_date=date.today())
            invoices.append(inv)
            print(f"> Fatura gerada: {inv}")

        elif choice == "8":
            if not invoices:
                print("> Nenhuma fatura gerada.")
            for inv in invoices:
                print(f"  - {inv} | {inv.get_status()}")

        elif choice == "9":
            if not customers:
                print("> Cadastre um cliente antes.")
                continue
            print("Selecione cliente por índice:")
            for i, c in enumerate(customers, 1):
                print(f"{i}. {c.name}")
            ci = int(input("Índice do cliente: ")) - 1

            desc = input("Descrição do problema: ")
            ticket = SupportTicket(
                customer=customers[ci],
                issue_description=desc,
                open_date=date.today()
            )
            tickets.append(ticket)
            print(f"> Chamado aberto: {ticket}")

        elif choice == "10":
            if not tickets:
                print("> Nenhum chamado cadastrado.")
            for t in tickets:
                print(f"  - {t} | {t.get_status()}")

        elif choice == "0":
            # auto-save antes de sair
            save_data(customers, plans, contracts, invoices, tickets)
            print(f"> Dados salvos em {DATA_FILE}")
            print("Saindo… até a próxima!")
            break

        else:
            print("> Opção inválida.")

if __name__ == "__main__":
    main()