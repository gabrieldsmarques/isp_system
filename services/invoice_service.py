from models.invoice import Invoice
from datetime import date
from typing import List

def generate_invoice(invoices: List[Invoice], contract, issue_date: date) -> Invoice:
    inv = Invoice(contract=contract, issue_date=issue_date)
    invoices.append(inv)
    return inv

def list_invoices(invoices: List[Invoice]) -> List[str]:
    return [f"{i} | {i.get_status()}" for i in invoices]

def pay_invoice(invoice, pay_date: date) -> bool:
    if invoice.paid:
        return False
    invoice.pay(pay_date)
    return True

def remove_invoice(invoices: List[Invoice], index: int) -> Invoice:
    return invoices.pop(index)
