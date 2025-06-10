import unittest
from services.plan_service import add_plan, list_plans, update_plan, remove_plan
from models.plan import Plan

class PlanServiceTest(unittest.TestCase):

    def test_add_plan_success(self):
        plans = []
        plan = add_plan(plans, name="Basic", speed_str="50", fee_str="79.9")
        self.assertIsInstance(plan, Plan)
        self.assertEqual(plan.name, "Basic")
        self.assertEqual(plan.speed_mbps, 50.0)
        self.assertEqual(plan.monthly_fee, 79.9)
        self.assertEqual(len(plans), 1)

    def test_add_plan_invalid_speed(self):
        plans = []
        # velocidade negativa
        plan = add_plan(plans, name="BadSpeed", speed_str="-10", fee_str="50")
        self.assertIsNone(plan)
        self.assertEqual(plans, [])

        # velocidade não numérica
        plan = add_plan(plans, name="NoSpeed", speed_str="fast", fee_str="50")
        self.assertIsNone(plan)
        self.assertEqual(plans, [])

    def test_add_plan_invalid_fee(self):
        plans = []
        # mensalidade zero
        plan = add_plan(plans, name="Free", speed_str="10", fee_str="0")
        self.assertIsNone(plan)
        self.assertEqual(plans, [])

        # mensalidade texto
        plan = add_plan(plans, name="TextFee", speed_str="10", fee_str="cheap")
        self.assertIsNone(plan)
        self.assertEqual(plans, [])

    def test_list_plans(self):
        # lista vazia
        self.assertEqual(list_plans([]), [])

        # lista não vazia
        plans = [Plan(name="A", speed_mbps=10, monthly_fee=20),
                 Plan(name="B", speed_mbps=100, monthly_fee=200)]
        descs = list_plans(plans)
        self.assertEqual(len(descs), 2)
        self.assertIn("Plan A: 10.0 Mbps for $ 20.00/month", descs[0])
        self.assertIn("Plan B: 100.0 Mbps for $ 200.00/month", descs[1])

    def test_update_plan_success(self):
        plans = [Plan(name="X", speed_mbps=5, monthly_fee=30)]
        p = plans[0]
        ok = update_plan(p, new_name="Y", speed_str="50", fee_str="60")
        self.assertTrue(ok)
        self.assertEqual(p.name, "Y")
        self.assertEqual(p.speed_mbps, 50.0)
        self.assertEqual(p.monthly_fee, 60.0)

    def test_update_plan_partial(self):
        plans = [Plan(name="Old", speed_mbps=5, monthly_fee=30)]
        p = plans[0]
        # apenas nome
        ok = update_plan(p, new_name="New", speed_str="", fee_str="")
        self.assertTrue(ok)
        self.assertEqual(p.name, "New")
        # velocidade e fee mantidos
        self.assertEqual(p.speed_mbps, 5)
        self.assertEqual(p.monthly_fee, 30)

    def test_update_plan_invalid_inputs(self):
        plans = [Plan(name="Z", speed_mbps=10, monthly_fee=40)]
        p = plans[0]
        # nova velocidade inválida
        ok = update_plan(p, new_name="", speed_str="zero", fee_str="")
        self.assertFalse(ok)
        # sem alterações
        self.assertEqual(p.speed_mbps, 10)
        self.assertEqual(p.monthly_fee, 40)

    def test_remove_plan(self):
        plans = [Plan(name="ToRemove", speed_mbps=1, monthly_fee=5)]
        removed = remove_plan(plans, 0)
        self.assertIsInstance(removed, Plan)
        self.assertEqual(removed.name, "ToRemove")
        self.assertEqual(plans, [])

if __name__ == "__main__":
    unittest.main()
