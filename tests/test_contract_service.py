import unittest
from datetime import date, timedelta
from services.contract_service import (
    create_contract, list_contracts,
    cancel_contract, reactivate_contract, remove_contract
)
from models.customer import Customer
from models.plan import Plan
from models.contract import Contract

class ContractServiceTest(unittest.TestCase):

    def setUp(self):
        # cria um cliente e um plano para usar nos testes
        self.customer = Customer(cpf="12345678901", name="Teste", address="Rua Teste, 123")
        self.plan = Plan(name="PlanoX", speed_mbps=100.0, monthly_fee=150.0)
        self.contracts = []

    def test_create_contract_success(self):
        start = date.today()
        ctr = create_contract(self.contracts, self.customer, self.plan, start)
        self.assertIsInstance(ctr, Contract)
        self.assertTrue(ctr.active)
        self.assertEqual(ctr.start_date, start)
        self.assertEqual(len(self.contracts), 1)
        # verificar que o contrato foi anexado ao cliente
        self.assertIs(self.customer.contract, ctr)

    def test_list_contracts_empty(self):
        self.assertEqual(list_contracts([]), [])

    def test_list_contracts_non_empty(self):
        ctr = create_contract(self.contracts, self.customer, self.plan, date.today())
        descs = list_contracts(self.contracts)
        self.assertEqual(len(descs), 1)
        self.assertIn("Ativo", descs[0])
        self.assertIn("PlanoX", descs[0])
        self.assertIn("Teste", descs[0])

    def test_cancel_contract_success(self):
        ctr = create_contract(self.contracts, self.customer, self.plan, date.today())
        cancel_date = date.today()
        ok = cancel_contract(ctr, cancel_date)
        self.assertTrue(ok)
        self.assertFalse(ctr.active)
        self.assertEqual(ctr.end_date, cancel_date)

    def test_cancel_contract_already_inactive(self):
        ctr = create_contract(self.contracts, self.customer, self.plan, date.today())
        cancel_contract(ctr, date.today())
        ok = cancel_contract(ctr, date.today())
        self.assertFalse(ok)

    def test_reactivate_contract_success(self):
        ctr = create_contract(self.contracts, self.customer, self.plan, date.today())
        cancel_contract(ctr, date.today())
        new_start = date.today() + timedelta(days=1)
        ok = reactivate_contract(ctr, new_start)
        self.assertTrue(ok)
        self.assertTrue(ctr.active)
        self.assertEqual(ctr.start_date, new_start)
        self.assertIsNone(ctr.end_date)

    def test_reactivate_contract_already_active(self):
        ctr = create_contract(self.contracts, self.customer, self.plan, date.today())
        ok = reactivate_contract(ctr, date.today())
        self.assertFalse(ok)

    def test_remove_contract(self):
        ctr = create_contract(self.contracts, self.customer, self.plan, date.today())
        removed = remove_contract(self.contracts, 0)
        self.assertIsInstance(removed, Contract)
        self.assertEqual(removed, ctr)
        self.assertEqual(self.contracts, [])

if __name__ == "__main__":
    unittest.main()
