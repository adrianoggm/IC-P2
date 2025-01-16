# tests/test_fitness.py

import unittest
import numpy as np
from src.fitness import calcular_coste, fitness_pop

class TestFitness(unittest.TestCase):
    def test_calcular_coste_basico(self):
        flujo_matrix = np.array([[0, 1], [1, 0]])
        distancia_matrix = np.array([[0.0, 2.0], [2.0, 0.0]])
        individuo = [0, 1]
        expected_cost = 0*0 + 1*2 + 1*2 + 0*0  # = 4.0
        self.assertEqual(calcular_coste(individuo, flujo_matrix, distancia_matrix), expected_cost)

    def test_calcular_coste_mayor(self):
        flujo_matrix = np.array([[0, 3], [3, 0]])
        distancia_matrix = np.array([[0.0, 1.5], [1.5, 0.0]])
        individuo = [1, 0]
        expected_cost = 0*0 + 3*1.5 + 3*1.5 + 0*0  # = 9.0
        self.assertEqual(calcular_coste(individuo, flujo_matrix, distancia_matrix), expected_cost)

    def test_fitness_pop(self):
        # Población de 2 individuos
        population = np.array([
            [0, 1],
            [1, 0]
        ])
        flujo_matrix = np.array([[0, 1], [1, 0]])
        distancia_matrix = np.array([[0.0, 2.0], [2.0, 0.0]])
        expected_fitness = np.array([4.0, 4.0])
        np.testing.assert_array_equal(fitness_pop(population, flujo_matrix, distancia_matrix), expected_fitness)

    def test_fitness_pop_varios_individuos(self):
        # Población de 3 individuos
        population = np.array([
            [0, 1, 2],
            [2, 1, 0],
            [1, 2, 0]
        ])
        flujo_matrix = np.array([
            [0, 2, 1],
            [2, 0, 3],
            [1, 3, 0]
        ])
        distancia_matrix = np.array([
            [0.0, 1.0, 2.0],
            [1.0, 0.0, 1.5],
            [2.0, 1.5, 0.0]
        ])
        # Calcular fitness manualmente
        # Individuo 0: [0,1,2]
        # Coste = 0*0 + 2*1 + 1*2 + 2*1 + 0*0 + 3*1.5 + 1*2 + 3*1.5 + 0*0 = 0 + 2 + 2 + 2 + 0 + 4.5 + 2 + 4.5 + 0 = 17.0
        # Individuo 1: [2,1,0]
        # Coste = 0*0 + 2*1 + 1*2 + 2*1 + 0*0 + 3*1.5 + 1*2 + 3*1.5 + 0*0 = 0 + 2 + 2 + 2 + 0 + 4.5 + 2 + 4.5 + 0 = 17.0
        # Individuo 2: [1,2,0]
        # Coste = 0*0 + 2*2 + 1*1 + 2*2 + 0*0 + 3*1.5 + 1*1 + 3*1.5 + 0*0 = 0 + 4 + 1 + 4 + 0 + 4.5 + 1 + 4.5 + 0 = 19.0
        expected_fitness = np.array([17.0, 16.0, 20.0])
        np.testing.assert_array_equal(fitness_pop(population, flujo_matrix, distancia_matrix), expected_fitness)

if __name__ == '__main__':
    unittest.main()