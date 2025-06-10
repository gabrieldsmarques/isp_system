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
