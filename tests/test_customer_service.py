import unittest
from services.customer_service import add_customer, list_customers, update_customer, remove_customer
from models.customer import Customer

class CustomerServiceTest(unittest.TestCase):

    def test_add_customer_success(self):
        customers = []
        cust = add_customer(customers, cpf="12345678901", name="Ana Silva", address="Rua A, 123")
        self.assertIsInstance(cust, Customer)
        self.assertEqual(cust.cpf, "12345678901")
        self.assertEqual(len(customers), 1)

    def test_add_customer_duplicate_cpf(self):
        customers = [Customer(cpf="12345678901", name="X", address="Y")]
        cust = add_customer(customers, cpf="12345678901", name="Outro", address="Z")
        self.assertIsNone(cust)
        self.assertEqual(len(customers), 1)

    def test_list_customers_empty(self):
        self.assertEqual(list_customers([]), [])

    def test_update_and_remove_customer(self):
        customers = [Customer(cpf="11122233344", name="João", address="Av. B, 45")]
        update_customer(customers[0], new_name="João P.", new_address="Av. C, 67")
        self.assertEqual(customers[0].name, "João P.")
        self.assertEqual(customers[0].address, "Av. C, 67")
        removed = remove_customer(customers, 0)
        self.assertEqual(removed.cpf, "11122233344")
        self.assertEqual(customers, [])

if __name__ == "__main__":
    unittest.main()
