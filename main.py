from datetime import date, timedelta
from model.customer import Customer
from model.plan import Plan
from model.contract import Contract
from model.invoice import Invoice
from model.support_ticket import SupportTicket
from persistence import JsonPersistence

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
    print("11. Salvar dados")
    print("12. Carregar dados")
    print("0. Sair")
    return input("Escolha uma opção: ").strip()

def main():
    customers = []
    plans = []
    contracts = []
    invoices = []
    tickets = []

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

            start = date.today()
            ctr = Contract(customer=customers[ci], plan=plans[pi], start_date=start)
            contracts.append(ctr)
            print(f"> Contrato criado: {ctr}")

        elif choice == "6":
            if not contracts:
                print("> Nenhum contrato criado.")
            for ctr in contracts:
                print(f"  - {ctr} | {ctr.get_status()}")

        elif choice == "7":
            if not contracts:
                print("> É necessário ao menos um contrato ativo.")
                continue
            print("Selecione contrato para faturar:")
            ativos = [c for c in contracts if c.active]
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

        elif choice == "11":
            filename = input("Nome do arquivo para salvar [data.json]: ").strip() or "data.json"
            data = {
                "customers": [c.to_dict() for c in customers],
                "plans": [p.to_dict() for p in plans],
                "contracts": [c.to_dict() for c in contracts],
                "invoices": [i.to_dict() for i in invoices],
                "support_tickets": [t.to_dict() for t in tickets],
            }
            JsonPersistence.save(filename, data)
            print(f"> Dados salvos em {filename}")

        elif choice == "12":
            filename = input("Nome do arquivo para carregar [data.json]: ").strip() or "data.json"
            try:
                raw = JsonPersistence.load(filename)
            except FileNotFoundError:
                print(f"> Arquivo não encontrado: {filename}")
                continue
            print("> Dados carregados (raw):")
            print(raw)

        elif choice == "0":
            print("Saindo… até a próxima!")
            break

        else:
            print("> Opção inválida.")

if __name__ == "__main__":
    main()