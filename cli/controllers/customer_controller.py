from models.customer import Customer
from validators.input_validators import valid_cpf
from cli.utils import select_or_search


def handle_add_customer(customers: list[Customer]) -> None:
    cpf = input("CPF (11 dígitos): ").strip()
    if not valid_cpf(cpf, {c.cpf for c in customers}):
        return
    name = input("Nome: ").strip()
    address = input("Endereço: ").strip()
    customers.append(Customer(cpf=cpf, name=name, address=address))
    print("> Cliente adicionado.")

def handle_list_customers(customers: list[Customer]) -> None:
    if not customers:
        print("> Nenhum cliente cadastrado.")
        return
    for c in customers:
        print(f" - {c} | {c.get_status()}")

def handle_edit_customer(customers: list[Customer]) -> None:
    idx = select_or_search(customers, "cliente", attr="cpf")
    if idx is None:
        return
    c = customers[idx]
    new_name = input(f"Novo nome [{c.name}]: ").strip() or c.name
    new_address = input(f"Novo endereço [{c.address}]: ").strip() or c.address
    c.name = new_name
    c.address = new_address
    print("> Cliente atualizado.")

def handle_remove_customer(customers: list[Customer]) -> None:
    idx = select_or_search(customers, "cliente", attr="cpf")
    if idx is None:
        return
    removed = customers.pop(idx)
    print(f"> Cliente removido: {removed}")
