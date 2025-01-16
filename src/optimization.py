# src/optimization.py

import numpy as np
import logging

def calcular_coste(individuo, flujo_matrix, distancia_matrix):
    """
    Calcula el coste total de una asignación según las matrices de flujo y distancia.

    Args:
        individuo (numpy.ndarray): Permutación que representa la asignación de instalaciones, shape=(n,).
        flujo_matrix (numpy.ndarray): Matriz de flujos, shape=(n, n).
        distancia_matrix (numpy.ndarray): Matriz de distancias, shape=(n, n).

    Returns:
        float: Coste total de la asignación.
    """
    try:
        # Multiplicación elemento a elemento y sumatoria
        coste = np.sum(flujo_matrix * distancia_matrix[individuo[:, np.newaxis], individuo[np.newaxis, :]])
        return coste
    except Exception as e:
        logging.error(f"Error al calcular el coste: {e}")
        raise

def optimizacion_2opt(individuo, flujo_matrix, distancia_matrix):
    """
    Aplica la optimización local 2-opt a un individuo.

    Args:
        individuo (numpy.ndarray): Individuo a optimizar, shape=(n,).
        flujo_matrix (numpy.ndarray): Matriz de flujos, shape=(n, n).
        distancia_matrix (numpy.ndarray): Matriz de distancias, shape=(n, n).

    Returns:
        tuple: Individuo optimizado y su coste.
    """
    mejor_individuo = individuo.copy()
    mejor_coste = calcular_coste(mejor_individuo, flujo_matrix, distancia_matrix)
    n = len(individuo)
    mejorado = False

    for i in range(1, n - 1):
        for j in range(i + 1, n):
            # Generar una nueva permutación con el segmento invertido
            nuevo_individuo = mejor_individuo.copy()
            nuevo_individuo[i:j] = mejor_individuo[j-1:i-1:-1]
            nuevo_coste = calcular_coste(nuevo_individuo, flujo_matrix, distancia_matrix)

            # Si la nueva permutación tiene un coste menor, actualizar
            if nuevo_coste < mejor_coste:
                mejor_individuo = nuevo_individuo
                mejor_coste = nuevo_coste
                mejorado = True
                break  # Salir del bucle interno para buscar nuevas mejoras
        if mejorado:
            break  # Salir del bucle externo si ya se realizó una mejora

    return mejor_individuo, mejor_coste