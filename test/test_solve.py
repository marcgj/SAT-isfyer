from main import Formula, WalkSat
import unittest
import sys

sys.path.append('..')


class TestUnsat(unittest.TestCase):
    def test_small(self):
        formula = Formula("test/formulas/unsat_small.cnf")
        sat = WalkSat(formula, max_tries=500)
        res = sat.solve()
        self.assertIsNone(res)

    def test_large(self):
        formula = Formula("test/formulas/unsat_large.cnf")
        sat = WalkSat(formula, max_tries=100)
        res = sat.solve()
        self.assertIsNone(res)


class TestSat(unittest.TestCase):
    def test_not_none(self):
        formula = Formula("test/formulas/sat_small.cnf")
        sat = WalkSat(formula)
        res = sat.solve()
        self.assertIsNotNone(res)

    def test_good_solution(self):
        formula = Formula("test/formulas/sat_small.cnf")
        sat = WalkSat(formula)
        res = sat.solve()
        self.assertIsNotNone(formula.deep_check_solution(res))


if __name__ == '__main__':
    unittest.main()
