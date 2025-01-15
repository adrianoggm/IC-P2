# tests/test_mutation.py

import unittest
import numpy as np
import random
from src.mutation import mutacion_swap

class TestMutation(unittest.TestCase):
    def setUp(self):
        # Fijar la semilla para reproducibilidad
        self.seed = 42
        random.seed(self.seed)
        np.random.seed(self.seed)
    
    def test_mutacion_swap_no_mutacion(self):
        individuo = np.array([0, 1, 2, 3, 4])
        # Forzar tasa_mutacion=0 para evitar mutación
        mutado = mutacion_swap(individuo, tasa_mutacion=0.0)
        np.testing.assert_array_equal(mutado, individuo)
    
    def test_mutacion_swap_con_mutacion(self):
        individuo = np.array([0, 1, 2, 3, 4])
        # Con semilla 42 y tasa_mutacion=1, los índices a intercambiar deberían ser predecibles
        mutado = mutacion_swap(individuo, tasa_mutacion=1.0)
        # Dependerá de la implementación de random.sample con la semilla 42, ajusta según sea necesario
        expected = np.array([0, 4, 2, 3, 1])  # Ajusta según el comportamiento esperado
        np.testing.assert_array_equal(mutado, expected)

if __name__ == '__main__':
    unittest.main()
