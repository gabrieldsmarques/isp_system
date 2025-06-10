from cli.utils import select_from_list
from services.invoice_service import (
    generate_invoice, list_invoices,
    pay_invoice, remove_invoice
)
from models.invoice import Invoice
from datetime import date
from exceptions import InvoiceAlreadyPaidError

def handle_generate_invoice(contracts: list, invoices: list[Invoice]) -> None:
    ativos = [c for c in contracts if c.active]
    if not ativos:
        print("> Nenhum contrato ativo.")
        return
    idx = select_from_list(ativos, "contrato ativo")
    if idx is None:
        return
    inv = generate_invoice(invoices, ativos[idx], date.today())
    print("> Fatura gerada.")

def handle_list_invoices(invoices: list[Invoice]) -> None:
    if not invoices:
        print("> Nenhuma fatura.")
        return
    for desc in list_invoices(invoices):
        print(" - " + desc)

def handle_pay_invoice(invoices: list[Invoice]) -> None:
    idx = select_from_list(invoices, "fatura")
    if idx is None:
        return
    try:
        pay_invoice(invoices[idx], date.today())
        print("> Fatura paga.")
    except InvoiceAlreadyPaidError as e:
        print(f"> {e}")

def handle_remove_invoice(invoices: list[Invoice]) -> None:
    idx = select_from_list(invoices, "fatura")
    if idx is None:
        return
    removed = remove_invoice(invoices, idx)
    print(f"> Fatura removida: {removed}")
