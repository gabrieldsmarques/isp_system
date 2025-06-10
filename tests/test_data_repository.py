import unittest
import os
import json
import tempfile
from datetime import date
from repositories.data_repository import DataRepository
from models.customer import Customer
from models.plan import Plan
from models.contract import Contract
from models.invoice import Invoice
from models.support_ticket import SupportTicket

class DataRepositoryTest(unittest.TestCase):

    def setUp(self):
        # Cria um arquivo temporário para usar como data.json
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        # Esvaziamos qualquer conteúdo inicial
        with open(self.path, "w") as f:
            f.write("{}")
        self.repo = DataRepository(filename=self.path)

        # Exemplos de dados
        self.customer = Customer(cpf="11122233344", name="Teste", address="Rua T, 1")
        self.plan = Plan(name="P1", speed_mbps=10.0, monthly_fee=50.0)
        self.contract = Contract(customer=self.customer, plan=self.plan, start_date=date.today())
        self.invoice = Invoice(contract=self.contract, issue_date=date.today())
        self.ticket = SupportTicket(customer=self.customer, issue_description="X", open_date=date.today())

    def tearDown(self):
        # Remove o arquivo temporário
        os.remove(self.path)

    def test_save_and_load_empty(self):
        # Quando não houver listas, load deve retornar listas vazias
        os.remove(self.path)
        repo = DataRepository(filename=self.path)
        customers, plans, contracts, invoices, tickets = repo.load()
        self.assertEqual(customers, [])
        self.assertEqual(plans, [])
        self.assertEqual(contracts, [])
        self.assertEqual(invoices, [])
        self.assertEqual(tickets, [])

    def test_save_and_load_with_data(self):
        # Prepara listas com os objetos
        customers = [self.customer]
        plans = [self.plan]
        contracts = [self.contract]
        invoices = [self.invoice]
        tickets = [self.ticket]

        # Salva no arquivo temporário
        self.repo.save(customers, plans, contracts, invoices, tickets)

        # Carrega de volta
        loaded = self.repo.load()
        self.assertEqual(len(loaded[0]), 1)  # customers
        self.assertEqual(len(loaded[1]), 1)  # plans
        self.assertEqual(len(loaded[2]), 1)  # contracts
        self.assertEqual(len(loaded[3]), 1)  # invoices
        self.assertEqual(len(loaded[4]), 1)  # tickets

        # Verifica atributos de um customer carregado
        cust_loaded = loaded[0][0]
        self.assertEqual(cust_loaded.cpf, self.customer.cpf)
        self.assertEqual(cust_loaded.name, self.customer.name)
        self.assertEqual(cust_loaded.address, self.customer.address)

        # Verifica que o contrato reanexou o customer
        ctr_loaded = loaded[2][0]
        self.assertIs(ctr_loaded.customer, cust_loaded)

        # Verifica invoice e ticket
        inv_loaded = loaded[3][0]
        self.assertEqual(inv_loaded.contract, ctr_loaded)
        tick_loaded = loaded[4][0]
        self.assertIs(tick_loaded.customer, cust_loaded)

if __name__ == "__main__":
    unittest.main()
