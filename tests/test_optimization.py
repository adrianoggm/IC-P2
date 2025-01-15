# tests/test_optimization.py

import unittest
import numpy as np
from src.optimization import optimizacion_2opt, calcular_coste

class TestOptimization(unittest.TestCase):
    def setUp(self):
        # Fijar la semilla para reproducibilidad
        self.seed = 42
        np.random.seed(self.seed)
    
    def test_optimizacion_2opt_mejora(self):
        # Crear un individuo con una asignación no óptima
        individuo = np.array([0, 2, 1, 3])
        flujo_matrix = np.array([
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0]
        ])
        distancia_matrix = np.array([
            [0.0, 1.0, 2.0, 3.0],
            [1.0, 0.0, 1.5, 2.5],
            [2.0, 1.5, 0.0, 1.0],
            [3.0, 2.5, 1.0, 0.0]
        ])
        optimizado, coste = optimizacion_2opt(individuo, flujo_matrix, distancia_matrix)
        # Verificar que el coste disminuye
        coste_original = calcular_coste(individuo, flujo_matrix, distancia_matrix)
        self.assertTrue(coste < coste_original)
    
    def test_optimizacion_2opt_no_mejora(self):
        # Crear un individuo que ya está optimizado
        individuo = np.array([0, 1, 2, 3])
        flujo_matrix = np.array([
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0]
        ])
        distancia_matrix = np.array([
            [0.0, 1.0, 2.0, 3.0],
            [1.0, 0.0, 1.5, 2.5],
            [2.0, 1.5, 0.0, 1.0],
            [3.0, 2.5, 1.0, 0.0]
        ])
        optimizado, coste = optimizacion_2opt(individuo, flujo_matrix, distancia_matrix)
        # El individuo ya está optimizado, por lo que debe permanecer igual
        self.assertTrue(np.array_equal(optimizado, individuo))
        self.assertEqual(coste, calcular_coste(individuo, flujo_matrix, distancia_matrix))

if __name__ == '__main__':
    unittest.main()