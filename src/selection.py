# src/selection.py

import numpy as np
import random

def seleccion_torneo(poblacion, fitness, k=3):
    """
    Selecciona un individuo de la población usando la selección por torneo.

    Args:
        poblacion (numpy.ndarray): Población de individuos, shape=(poblacion, n).
        fitness (numpy.ndarray): Fitness correspondiente a cada individuo, shape=(poblacion,).
        k (int, optional): Número de individuos a seleccionar para el torneo.

    Returns:
        numpy.ndarray: Individuo seleccionado.
    """
    # Seleccionar k individuos al azar
    seleccionados = np.random.choice(len(poblacion), size=k, replace=False)
    # Encontrar el índice del individuo con el mejor fitness (menor coste)
    mejor_idx = seleccionados[np.argmin(fitness[seleccionados])]
    return poblacion[mejor_idx]