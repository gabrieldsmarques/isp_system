from datetime import date
from typing import List, Tuple
from persistence.persistence import JsonPersistence
from models.customer import Customer
from models.plan import Plan
from models.contract import Contract
from models.invoice import Invoice
from models.support_ticket import SupportTicket

class DataRepository:
    """
    Encapsula carregamento e salvamento de todas as entidades do sistema.
    """

    def __init__(self, filename: str = "data.json"):
        self.filename = filename

    def load(self) -> Tuple[
        List[Customer], List[Plan], List[Contract],
        List[Invoice], List[SupportTicket]
    ]:
        try:
            raw = JsonPersistence.load(self.filename)
        except FileNotFoundError:
            return [], [], [], [], []

        # Reconstrução de clientes
        customers: List[Customer] = []
        for rd in raw.get("customers", []):
            customers.append(Customer.from_dict(rd))

        # Planos
        plans: List[Plan] = []
        for rd in raw.get("plans", []):
            plans.append(Plan.from_dict(rd))

        # Contratos
        contracts: List[Contract] = []
        cust_map = {c.cpf: c for c in customers}
        plan_map = {p.name: p for p in plans}
        for rd in raw.get("contracts", []):
            contracts.append(Contract.from_dict(rd, cust_map, plan_map))

        # Faturas
        invoices: List[Invoice] = []
        ctr_map = {c.customer.cpf: c for c in contracts}
        for rd in raw.get("invoices", []):
            invoices.append(Invoice.from_dict(rd, ctr_map))

        # Chamados
        tickets: List[SupportTicket] = []
        for rd in raw.get("support_tickets", []):
            tickets.append(SupportTicket.from_dict(rd, cust_map))

        return customers, plans, contracts, invoices, tickets

    def save(
        self,
        customers: List[Customer], plans: List[Plan],
        contracts: List[Contract], invoices: List[Invoice],
        tickets: List[SupportTicket]
    ) -> None:
        data = {
            "customers": [c.to_dict() for c in customers],
            "plans":     [p.to_dict() for p in plans],
            "contracts": [c.to_dict() for c in contracts],
            "invoices":  [i.to_dict() for i in invoices],
            "support_tickets": [t.to_dict() for t in tickets],
        }
        JsonPersistence.save(self.filename, data)
