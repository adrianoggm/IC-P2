# src/crossover.py

import numpy as np
import random
import logging

def cruce_pmx(parent1, parent2):
    """
    Realiza el cruce PMX entre dos padres.

    Args:
        parent1 (list o numpy.ndarray): Primer padre, shape=(n,).
        parent2 (list o numpy.ndarray): Segundo padre, shape=(n,).

    Returns:
        tuple: Dos hijos resultantes del cruce, cada uno shape=(n,).
    """
    # Convertir padres a arreglos de NumPy si no lo son
    parent1 = np.array(parent1)
    parent2 = np.array(parent2)

    size = len(parent1)
    hijo1, hijo2 = [-1]*size, [-1]*size

    # Elegir dos puntos de cruce al azar
    punto1, punto2 = sorted(random.sample(range(size), 2))
    logging.debug(f"Puntos de cruce seleccionados: {punto1}, {punto2}")

    # Copiar los segmentos de los padres a los hijos
    hijo1[punto1:punto2] = parent1[punto1:punto2]
    hijo2[punto1:punto2] = parent2[punto1:punto2]
    logging.debug(f"Hijo1 después de copiar segmento: {hijo1}")
    logging.debug(f"Hijo2 después de copiar segmento: {hijo2}")

    def completar_hijo(hijo, parent, parent_original):
        """
        Completa el hijo con elementos del otro padre según el mapeo de PMX.

        Args:
            hijo (list): Hijo parcialmente completado.
            parent (numpy.ndarray): Padre de donde se obtendrán los elementos faltantes.
            parent_original (numpy.ndarray): Padre original para el mapeo.

        Returns:
            list: Hijo completamente completado.
        """
        # Asegurarse de que 'parent' y 'parent_original' sean arreglos de NumPy
        parent = np.array(parent)
        parent_original = np.array(parent_original)

        size = len(hijo)
        for i in range(punto1, punto2):
            elemento = parent[i]
            logging.debug(f"Procesando elemento: {elemento}")
            if elemento not in hijo:
                try:
                    # Encontrar el índice donde 'parent' es igual a 'parent_original[i]'
                    pos_array = np.where(parent == parent_original[i])[0]
                    if pos_array.size == 0:
                        raise ValueError(f"Elemento {parent_original[i]} no encontrado en 'parent'")
                    pos = pos_array[0]
                    logging.debug(f"Posición encontrada para mapeo: {pos}")
                except Exception as e:
                    logging.error(f"Error al encontrar posición: {e}")
                    pos = 0  # Maneja el caso donde no se encuentra

                # Encontrar una posición válida donde 'hijo[pos]' es -1
                while hijo[pos] != -1:
                    try:
                        pos_array = np.where(parent == parent_original[pos])[0]
                        if pos_array.size == 0:
                            raise ValueError(f"Elemento {parent_original[pos]} no encontrado en 'parent'")
                        pos = pos_array[0]
                        logging.debug(f"Posición mapeada siguiente: {pos}")
                    except Exception as e:
                        logging.error(f"Error al mapear siguiente posición: {e}")
                        pos = 0  # Maneja el caso donde no se encuentra
                        break

                hijo[pos] = elemento
                logging.debug(f"Hijo actualizado en posición {pos}: {hijo}")

        # Rellenar los -1 con los elementos restantes del padre
        for i in range(size):
            if hijo[i] == -1:
                hijo[i] = parent[i]
                logging.debug(f"Hijo completado en posición {i}: {hijo}")

        return hijo

    # Completar los hijos
    hijo1 = completar_hijo(hijo1, parent2, parent1)
    hijo2 = completar_hijo(hijo2, parent1, parent2)

    # Convertir hijos a arreglos de NumPy antes de retornarlos
    return np.array(hijo1), np.array(hijo2)