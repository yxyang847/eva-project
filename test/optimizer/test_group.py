import unittest

from mock import MagicMock

from src.optimizer.group import Group
from src.optimizer.group_expression import GroupExpression
from src.optimizer.property import Property, PropertyType


class TestGroup(unittest.TestCase):
    def test_simple_add_group_expr(self):
        grp = Group(0)

        grp_expr1 = GroupExpression(MagicMock())
        grp_expr1.opr.is_logical = lambda: True

        grp_expr2 = GroupExpression(MagicMock())
        grp_expr2.opr.is_logical = lambda: False

        grp_expr3 = GroupExpression(MagicMock(), 0)
        grp_expr3.opr.is_logical = lambda: True

        grp.add_expr(grp_expr1)
        self.assertEquals(len(grp.logical_exprs), 1)

        grp.add_expr(grp_expr2)
        self.assertEquals(len(grp.logical_exprs), 1)
        self.assertEquals(len(grp.physical_exprs), 1)

        grp.add_expr(grp_expr3)
        self.assertEquals(len(grp.logical_exprs), 2)
        self.assertEquals(len(grp.physical_exprs), 1)

    def test_add_group_expr_with_unmatched_group_id(self):
        grp = Group(0)

        grp_expr1 = GroupExpression(MagicMock(), 1)
        grp_expr1.opr.is_logical = lambda: True

        grp.add_expr(grp_expr1)
        self.assertEquals(len(grp.logical_exprs), 0)
        self.assertEquals(len(grp.physical_exprs), 0)

    def test_add_group_expr_cost(self):
        grp = Group(0)
        prpty = Property(PropertyType(1))

        grp_expr1 = GroupExpression(MagicMock(), 1)
        grp_expr1.opr.is_logical = lambda: True

        grp_expr2 = GroupExpression(MagicMock())
        grp_expr2.opr.is_logical = lambda: False

        grp.add_expr(grp_expr1)
        grp.add_expr_cost(grp_expr1, prpty, 1)

        grp.add_expr(grp_expr2)
        grp.add_expr_cost(grp_expr2, prpty, 0)

        self.assertEqual(grp.get_best_expr(prpty), grp_expr2)
        self.assertEqual(grp.get_best_expr_cost(prpty), 0)

    def test_empty_group_expr(self):
        grp = Group(0)
        prpty = Property(PropertyType(1))

        self.assertEqual(grp.get_best_expr(prpty), None)
        self.assertEqual(grp.get_best_expr_cost(prpty), None)
