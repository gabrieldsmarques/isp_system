from models.support_ticket import SupportTicket
from datetime import date
from typing import List

def open_ticket(tickets: List[SupportTicket], customer, description: str, open_date: date) -> SupportTicket:
    tick = SupportTicket(customer=customer, issue_description=description, open_date=open_date)
    tickets.append(tick)
    return tick

def list_tickets(tickets: List[SupportTicket]) -> List[str]:
    return [f"{t} | {t.get_status()}" for t in tickets]

def close_ticket(ticket, resolution: str, close_date: date) -> bool:
    if ticket.status == "Fechado":
        return False
    ticket.close(resolution=resolution, close_date=close_date)
    return True

def reopen_ticket(ticket, new_open_date: date) -> bool:
    if ticket.status == "Aberto":
        return False
    ticket.reopen(new_open_date=new_open_date)
    return True

def remove_ticket(tickets: List[SupportTicket], index: int) -> SupportTicket:
    return tickets.pop(index)
