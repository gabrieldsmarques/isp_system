from cli.utils import select_from_list
from services.plan_service import add_plan, list_plans, update_plan, remove_plan
from models.plan import Plan

def handle_add_plan(plans: list[Plan]) -> None:
    name = input("Nome do plano: ").strip()
    speed = input("Velocidade (Mbps): ").strip()
    fee = input("Mensalidade: ").strip()
    new = add_plan(plans, name, speed, fee)
    if new:
        print("> Plano adicionado.")

def handle_list_plans(plans: list[Plan]) -> None:
    if not plans:
        print("> Nenhum plano cadastrado.")
        return
    for desc in list_plans(plans):
        print(" - " + desc)

def handle_edit_plan(plans: list[Plan]) -> None:
    idx = select_from_list(plans, "plano")
    if idx is None:
        return
    p = plans[idx]
    new_name = input(f"Novo nome [{p.name}]: ").strip()
    speed = input(f"Nova velocidade [{p.speed_mbps}]: ").strip()
    fee = input(f"Nova mensalidade [{p.monthly_fee}]: ").strip()
    ok = update_plan(p, new_name, speed, fee)
    if ok:
        print("> Plano atualizado.")

def handle_remove_plan(plans: list[Plan]) -> None:
    idx = select_from_list(plans, "plano")
    if idx is None:
        return
    removed = remove_plan(plans, idx)
    print(f"> Plano removido: {removed}")
