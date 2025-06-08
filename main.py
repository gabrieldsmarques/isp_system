from datetime import date, timedelta
from model.customer import Customer
from model.plan import Plan
from model.contract import Contract
from model.invoice import Invoice
from model.support_ticket import SupportTicket
from persistence import JsonPersistence

if __name__ == "__main__":
    
    cliente1 = Customer(ssn="12345678900", name="Alice Silva", address="Rua das Flores, 123")
    plano_basico = Plan(name="Basic", speed_mbps=50.0, monthly_fee=79.90)
    hoje = date.today()
    contrato1 = Contract(customer=cliente1, plan=plano_basico, start_date=hoje)

    print(f"Cliente: {cliente1}")
    print(f"Plano contratado: {plano_basico}")
    print(f"Contrato criado: {contrato1}")
    print(f"Status do cliente: {cliente1.get_status()}")
    print(f"Status do contrato: {contrato1.get_status()}")

    # Emissão de fatura
    fatura1 = Invoice(contract=contrato1, issue_date=hoje)
    print(f"Fatura emitida: {fatura1}")
    print(f"Status da fatura: {fatura1.get_status()}")
    
    # Exemplo de pagamento
    data_pagamento = hoje + timedelta(days=5)
    fatura1.pay(pay_date=data_pagamento)
    print(f"Status da fatura após pagamento: {fatura1.get_status()}")
    
    
    
    # Abertura de chamado de suporte
    chamado1 = SupportTicket(
        customer=cliente1,
        issue_description="Internet intermitente nos finais de semana",
        open_date=hoje
    )
    print(f"Chamado aberto: {chamado1}")
    print(f"Status do chamado: {chamado1.get_status()}")

    # Encerrando chamado
    data_fechamento = hoje + timedelta(days=2)
    chamado1.close(
       resolution="Reinicialização do modem e ajuste de sinal concluídos",
        close_date=data_fechamento
    )
    print(f"Status do chamado após fechamento: {chamado1.get_status()}")
    
    # Persistência em JSON
    data = {
        "customers": [cliente1.to_dict()],
        "plans": [plano_basico.to_dict()],
        "contracts": [contrato1.to_dict()],
        "invoices": [fatura1.to_dict()],
        "support_tickets": [chamado1.to_dict()]
    }
    JsonPersistence.save("data.json", data)
    print("Dados salvos em data.json")

    # Carregamento e exibição
    loaded = JsonPersistence.load("data.json")
    print("Dados carregados:", loaded)