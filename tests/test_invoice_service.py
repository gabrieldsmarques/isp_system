import unittest
from datetime import date, timedelta
from models.customer import Customer
from models.plan import Plan
from models.contract import Contract
from models.invoice import Invoice
from services.invoice_service import (
    generate_invoice, list_invoices,
    pay_invoice, remove_invoice
)

class InvoiceServiceTest(unittest.TestCase):

    def setUp(self):
        # Criar cliente, plano e contrato para os testes
        self.customer = Customer(cpf="12345678901", name="Teste", address="Rua X, 123")
        self.plan = Plan(name="PlanoTest", speed_mbps=50.0, monthly_fee=100.0)
        self.contract = Contract(customer=self.customer, plan=self.plan, start_date=date.today())
        self.invoices = []

    def test_generate_invoice_success(self):
        today = date.today()
        inv = generate_invoice(self.invoices, self.contract, today)
        self.assertIsInstance(inv, Invoice)
        self.assertEqual(inv.contract, self.contract)
        self.assertEqual(inv.issue_date, today)
        self.assertEqual(inv.amount, self.plan.monthly_fee)
        self.assertEqual(inv.due_date, today + timedelta(days=30))
        self.assertFalse(inv.paid)
        self.assertIsNone(inv.paid_date)
        self.assertEqual(len(self.invoices), 1)

    def test_list_invoices_empty(self):
        self.assertEqual(list_invoices([]), [])

    def test_list_invoices_non_empty(self):
        inv = generate_invoice(self.invoices, self.contract, date.today())
        descs = list_invoices(self.invoices)
        self.assertEqual(len(descs), 1)
        # Descrição deve incluir o repr do invoice e seu status
        self.assertIn(str(inv), descs[0])
        self.assertIn("Aberta", descs[0])

    def test_pay_invoice_success(self):
        inv = generate_invoice(self.invoices, self.contract, date.today())
        pay_date = date.today()
        ok = pay_invoice(inv, pay_date)
        self.assertTrue(ok)
        self.assertTrue(inv.paid)
        self.assertEqual(inv.paid_date, pay_date)

    def test_pay_invoice_already_paid(self):
        inv = generate_invoice(self.invoices, self.contract, date.today())
        pay_invoice(inv, date.today())
        ok2 = pay_invoice(inv, date.today())
        self.assertFalse(ok2)

    def test_remove_invoice(self):
        inv = generate_invoice(self.invoices, self.contract, date.today())
        removed = remove_invoice(self.invoices, 0)
        self.assertIs(removed, inv)
        self.assertEqual(self.invoices, [])

if __name__ == "__main__":
    unittest.main()
