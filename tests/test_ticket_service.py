import unittest
from datetime import date
from models.customer import Customer
from models.support_ticket import SupportTicket
from services.support_ticket_service import (
    open_ticket, list_tickets,
    close_ticket, reopen_ticket, remove_ticket
)

class TicketServiceTest(unittest.TestCase):

    def setUp(self):
        # Criar um cliente e lista de tickets
        self.customer = Customer(cpf="99988877766", name="Cliente", address="Endereço")
        self.tickets = []

    def test_open_ticket(self):
        today = date.today()
        ticket = open_ticket(self.tickets, self.customer, "Problema X", today)
        self.assertIsInstance(ticket, SupportTicket)
        self.assertEqual(ticket.customer, self.customer)
        self.assertEqual(ticket.issue_description, "Problema X")
        self.assertEqual(ticket.open_date, today)
        self.assertEqual(ticket.status, "Aberto")
        self.assertIsNone(ticket.close_date)
        self.assertIn(ticket, self.tickets)

    def test_list_tickets_empty(self):
        self.assertEqual(list_tickets([]), [])

    def test_list_tickets_non_empty(self):
        ticket = open_ticket(self.tickets, self.customer, "Desc", date.today())
        descs = list_tickets(self.tickets)
        self.assertEqual(len(descs), 1)
        # Descrição deve conter repr do ticket e seu status aberto
        self.assertIn(str(ticket), descs[0])
        self.assertIn("Aberto", descs[0])

    def test_close_ticket_success(self):
        ticket = open_ticket(self.tickets, self.customer, "Desc", date.today())
        close_date = date.today()
        ok = close_ticket(ticket, "Resolvido", close_date)
        self.assertTrue(ok)
        self.assertEqual(ticket.status, "Fechado")
        self.assertEqual(ticket.resolution, "Resolvido")
        self.assertEqual(ticket.close_date, close_date)

    def test_close_ticket_already_closed(self):
        ticket = open_ticket(self.tickets, self.customer, "Desc", date.today())
        close_ticket(ticket, "Resolvido", date.today())
        ok2 = close_ticket(ticket, "Outra resolução", date.today())
        self.assertFalse(ok2)
        # Não deve sobrescrever a resolução anterior
        self.assertEqual(ticket.resolution, "Resolvido")

    def test_reopen_ticket_success(self):
        ticket = open_ticket(self.tickets, self.customer, "Desc", date.today())
        close_ticket(ticket, "Resolvido", date.today())
        new_open = date.today()
        ok = reopen_ticket(ticket, new_open)
        self.assertTrue(ok)
        self.assertEqual(ticket.status, "Aberto")
        self.assertEqual(ticket.open_date, new_open)
        self.assertIsNone(ticket.close_date)
        self.assertIsNone(ticket.resolution)

    def test_reopen_ticket_already_open(self):
        ticket = open_ticket(self.tickets, self.customer, "Desc", date.today())
        ok = reopen_ticket(ticket, date.today())
        self.assertFalse(ok)
        self.assertEqual(ticket.status, "Aberto")

    def test_remove_ticket(self):
        ticket = open_ticket(self.tickets, self.customer, "Desc", date.today())
        removed = remove_ticket(self.tickets, 0)
        self.assertIs(removed, ticket)
        self.assertEqual(self.tickets, [])

if __name__ == "__main__":
    unittest.main()
