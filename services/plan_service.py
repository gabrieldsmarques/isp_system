from models.plan import Plan
from validators.input_validators import valid_positive_number
from typing import List, Optional

def add_plan(plans: List[Plan], name: str, speed_str: str, fee_str: str) -> Optional[Plan]:
    speed = valid_positive_number(speed_str, "velocidade")
    if speed is None:
        return None
    fee = valid_positive_number(fee_str, "mensalidade")
    if fee is None:
        return None
    plan = Plan(name=name, speed_mbps=speed, monthly_fee=fee)
    plans.append(plan)
    return plan

def list_plans(plans: List[Plan]) -> List[str]:
    return [p.description() for p in plans]

def update_plan(plan: Plan, new_name: str, speed_str: str, fee_str: str) -> bool:
    plan.name = new_name or plan.name
    if speed_str:
        val = valid_positive_number(speed_str, "velocidade")
        if val is None:
            return False
        plan.speed_mbps = val
    if fee_str:
        val = valid_positive_number(fee_str, "mensalidade")
        if val is None:
            return False
        plan.monthly_fee = val
    return True

def remove_plan(plans: List[Plan], index: int) -> Plan:
    return plans.pop(index)
