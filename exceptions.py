class DomainError(Exception):
    """Erro genérico de domínio."""
    pass

class ContractInactiveError(DomainError):
    """Tentativa de cancelar um contrato já inativo."""
    pass

class ContractActiveError(DomainError):
    """Tentativa de reativar um contrato já ativo."""
    pass

class InvoiceAlreadyPaidError(DomainError):
    """Tentativa de pagar uma fatura já paga."""
    pass

class TicketAlreadyClosedError(DomainError):
    """Tentativa de fechar um chamado já fechado."""
    pass

class TicketAlreadyOpenError(DomainError):
    """Tentativa de reabrir um chamado já aberto."""
    pass
