# src/crossover.py

import numpy as np
import random

def cruce_pmx(parent1, parent2):
    """
    Realiza el cruce PMX entre dos padres.

    Args:
        parent1 (list o numpy.ndarray): Primer padre, shape=(n,).
        parent2 (list o numpy.ndarray): Segundo padre, shape=(n,).

    Returns:
        tuple: Dos hijos resultantes del cruce, cada uno shape=(n,).
    """
    size = len(parent1)
    hijo1, hijo2 = [-1]*size, [-1]*size

    # Elegir dos puntos de cruce al azar
    punto1, punto2 = sorted(random.sample(range(size), 2))

    # Copiar los segmentos de los padres a los hijos
    hijo1[punto1:punto2] = parent1[punto1:punto2]
    hijo2[punto1:punto2] = parent2[punto1:punto2]

    def completar_hijo(hijo, parent, parent_original):
        """
        Completa el hijo con elementos del otro padre según el mapeo de PMX.

        Args:
            hijo (list): Hijo parcialmente completado.
            parent (list o numpy.ndarray): Padre de donde se obtendrán los elementos faltantes.
            parent_original (list o numpy.ndarray): Padre original para el mapeo.

        Returns:
            list: Hijo completamente completado.
        """
        size = len(hijo)
        for i in range(punto1, punto2):
            elemento = parent[i]
            if elemento not in hijo:
                pos = i
                while True:
                    elemento_mapeado = parent_original[pos]
                    try:
                        pos = parent.index(elemento_mapeado)
                    except ValueError:
                        break
                    if hijo[pos] == -1:
                        hijo[pos] = elemento
                        break
                else:
                    break
        # Rellenar los -1 con los elementos restantes del padre
        for i in range(size):
            if hijo[i] == -1:
                hijo[i] = parent[i]
        return hijo

    # Completar los hijos
    hijo1 = completar_hijo(hijo1, parent2, parent1)
    hijo2 = completar_hijo(hijo2, parent1, parent2)

    return np.array(hijo1), np.array(hijo2)
