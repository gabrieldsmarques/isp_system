def select_from_list(lst: list, label: str) -> int | None:
    """
    Exibe uma lista enumerada e retorna o índice escolhido (0-based),
    ou None se não houver itens ou entrada inválida.
    """
    if not lst:
        print(f"> Nenhum {label} disponível.")
        return None
    for i, item in enumerate(lst, 1):
        print(f"{i}. {item}")
    try:
        idx = int(input(f"Índice do {label}: ").strip()) - 1
        if idx < 0 or idx >= len(lst):
            raise IndexError
        return idx
    except (ValueError, IndexError):
        print(f"> Índice inválido para {label}.")
        return None
    
def select_or_search(lst: list, label: str, attr: str = None) -> int | None:
    """
    Exibe lista e retorna índice escolhido,
    ou — se o usuário digitar um termo (ex: CPF) — busca o primeiro
    com atributo `attr` igual a esse termo.
    """
    if not lst:
        print(f"> Nenhum {label} disponível.")
        return None

    print(f"\nEscolha {label} por índice ou digite valor para buscar ({attr}):")
    for i, item in enumerate(lst, 1):
        # exibe item resumido
        print(f"{i}. {item}")
    entrada = input(f"{label} (índice ou valor): ").strip()

    # se for número e estiver no intervalo, usa índice
    if entrada.isdigit():
        idx = int(entrada) - 1
        if 0 <= idx < len(lst):
            return idx

    # senão, tenta buscar pelo atributo
    if attr:
        for i, item in enumerate(lst):
            if getattr(item, attr) == entrada:
                return i

    print(f"> Nenhum {label} encontrado para '{entrada}'.")
    return None
