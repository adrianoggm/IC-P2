# tests/test_selection.py

import unittest
import numpy as np
import random
from src.selection import seleccion_torneo

class TestSelection(unittest.TestCase):
    def setUp(self):
        # Fijar la semilla para reproducibilidad
        self.seed = 42
        random.seed(self.seed)
        np.random.seed(self.seed)
    
    def test_seleccion_torneo_basico(self):
        poblacion = np.array([
            [0, 1],
            [1, 0],
            [2, 3],
            [3, 2],
            [0,3],
            [3,0]
        ])
        fitness = np.array([10, 5, 8, 3,9,8])
       
        seleccionado = seleccion_torneo(poblacion, fitness, k=2)
        
        # Con la semilla 42, verifica el individuo seleccionado
        # Dependiendo de la implementación de selección, ajustar la verificación
        # Por ejemplo, podría seleccionar el segundo individuo
        
        self.assertTrue(np.array_equal(seleccionado, poblacion[1]))  # Ajusta según el comportamiento esperado

    
    def test_seleccion_torneo_con_mejor_fitness(self):
        poblacion = np.array([
            [0, 1],
            [1, 0],
            [2, 3],
            [3, 2]
        ])
        fitness = np.array([10, 5, 8, 3])
        seleccionado = seleccion_torneo(poblacion, fitness, k=3)
        # Con la semilla 42, verifica que se selecciona el mejor fitness=3
        self.assertTrue(np.array_equal(seleccionado, poblacion[3]))

if __name__ == '__main__':
    unittest.main()
