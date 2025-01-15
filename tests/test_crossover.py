# tests/test_crossover.py

import unittest
import numpy as np
from src.crossover import cruce_pmx

class TestCrossover(unittest.TestCase):
    def test_cruce_pmx(self):
        parent1 = [0, 1, 2, 3, 4]
        parent2 = [4, 3, 2, 1, 0]
        hijo1, hijo2 = cruce_pmx(parent1, parent2)
        # Verificar que los hijos sean permutaciones válidas
        self.assertEqual(sorted(hijo1), sorted(parent1))
        self.assertEqual(sorted(hijo2), sorted(parent2))

if __name__ == '__main__':
    unittest.main()