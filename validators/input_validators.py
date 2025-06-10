import re
from typing import Optional, Set

def valid_cpf(cpf: str, existing_cpfs: Set[str]) -> bool:
    """
    Valida CPF: 11 dígitos numéricos e não duplicado.
    """
    if not re.fullmatch(r"\d{11}", cpf):
        print("> CPF inválido: deve conter exatamente 11 dígitos numéricos.")
        return False
    if cpf in existing_cpfs:
        print("> CPF já cadastrado.")
        return False
    return True

def valid_positive_number(value: str, field_name: str) -> Optional[float]:
    """
    Converte string em float positivo; retorna None se inválido.
    """
    try:
        num = float(value)
        if num <= 0:
            raise ValueError
        return num
    except ValueError:
        print(f"> Valor inválido para {field_name}: deve ser número positivo.")
        return None
