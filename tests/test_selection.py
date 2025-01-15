# tests/test_selection.py

import unittest
import numpy as np
from src.selection import seleccion_torneo

class TestSelection(unittest.TestCase):
    def test_seleccion_torneo_basico(self):
        poblacion = np.array([
            [0, 1],
            [1, 0],
            [2, 3],
            [3, 2]
        ])
        fitness = np.array([10, 5, 8, 3])
        seleccionado = seleccion_torneo(poblacion, fitness, k=2)
        # Podría seleccionar cualquiera de los 4 individuos, pero en k=2 es probable que uno de los mejores
        self.assertIn(tuple(seleccionado), [tuple(poblacion[i]) for i in [0,1,2,3]])

    def test_seleccion_torneo_con_mejor_fitness(self):
        poblacion = np.array([
            [0, 1],
            [1, 0],
            [2, 3],
            [3, 2]
        ])
        fitness = np.array([10, 5, 8, 3])
        seleccionado = seleccion_torneo(poblacion, fitness, k=3)
        # En un torneo de 3, es más probable seleccionar el mejor (fitness=3)
        self.assertTrue(np.array_equal(seleccionado, poblacion[3]))

if __name__ == '__main__':
    unittest.main()