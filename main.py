from datetime import date, timedelta
from model.customer import Customer
from model.plan import Plan
from model.contract import Contract
from model.invoice import Invoice

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