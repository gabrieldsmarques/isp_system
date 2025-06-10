from cli.utils import select_from_list
from services.support_ticket_service import (
    open_ticket, list_tickets,
    close_ticket, reopen_ticket, remove_ticket
)
from models.support_ticket import SupportTicket
from datetime import date

def handle_open_ticket(customers: list, tickets: list[SupportTicket]) -> None:
    ci = select_from_list(customers, "cliente")
    if ci is None:
        return
    desc = input("Descrição do problema: ").strip()
    tick = open_ticket(tickets, customers[ci], desc, date.today())
    print("> Chamado aberto.")

def handle_list_tickets(tickets: list) -> None:
    if not tickets:
        print("> Nenhum chamado.")
        return
    for desc in list_tickets(tickets):
        print(" - " + desc)

def handle_close_ticket(tickets: list) -> None:
    idx = select_from_list(tickets, "chamado")
    if idx is None:
        return
    res = input("Resolução: ").strip()
    ok = close_ticket(tickets[idx], res, date.today())
    if ok:
        print("> Chamado fechado.")
    else:
        print("> Chamado já está fechado.")

def handle_reopen_ticket(tickets: list) -> None:
    idx = select_from_list(tickets, "chamado")
    if idx is None:
        return
    ok = reopen_ticket(tickets[idx], date.today())
    if ok:
        print("> Chamado reaberto.")
    else:
        print("> Chamado já está aberto.")

def handle_remove_ticket(tickets: list) -> None:
    idx = select_from_list(tickets, "chamado")
    if idx is None:
        return
    removed = remove_ticket(tickets, idx)
    print(f"> Chamado removido: {removed}")
