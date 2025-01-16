# tests/test_crossover.py

import unittest
import numpy as np
import random
import logging
from src.crossover import cruce_pmx

class TestCrossover(unittest.TestCase):
    def setUp(self):
        # Fijar la semilla para reproducibilidad
        self.seed = 42
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        # Configurar logging para las pruebas
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
    
    def test_cruce_pmx(self):
        parent1 = [0, 1, 2, 3, 4]
        parent2 = [4, 3, 2, 1, 0]
        hijo1, hijo2 = cruce_pmx(parent1, parent2)
        # Verificar que los hijos sean permutaciones válidas
        self.assertEqual(sorted(hijo1), sorted(parent1))
        self.assertEqual(sorted(hijo2), sorted(parent2))
        # Verificar que los segmentos copiados sean correctos
        # Dado que con la semilla 42, los puntos de cruce serán consistentes
        # Puedes agregar más aserciones según la implementación exacta

    def test_cruce_pmx_con_segmento(self):
        parent1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        parent2 = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        hijo1, hijo2 = cruce_pmx(parent1, parent2)
        # Verificar que los hijos sean permutaciones válidas
        self.assertEqual(sorted(hijo1), sorted(parent1))
        self.assertEqual(sorted(hijo2), sorted(parent2))
        # Verificar que los segmentos copiados sean correctos
        # Puedes agregar más aserciones específicas según los puntos de cruce

if __name__ == '__main__':
    unittest.main()
