# src/fitness.py

import numpy as np
import logging

def calcular_coste(individuo, flujo_matrix, distancia_matrix):
    """
    Calcula el coste total de una asignación según las matrices de flujo y distancia.

    Args:
        individuo (list o np.ndarray): Permutación que representa la asignación de instalaciones.
        flujo_matrix (numpy.ndarray): Matriz de flujos.
        distancia_matrix (numpy.ndarray): Matriz de distancias.

    Returns:
        int: Coste total de la asignación.
    """
    try:
        # Asegurarse de que 'individuo' es un array de NumPy
        individuo = np.array(individuo)
        coste_total = np.sum(flujo_matrix * distancia_matrix[individuo][:, individuo])
        return coste_total
    except Exception as e:
        logging.error(f"Error al calcular el coste: {e}")
        raise

def fitness_pop(population, flow, distances):
    """
    Calcula el fitness para una población completa de individuos de manera vectorizada.

    Args:
        population (numpy.ndarray): Matriz 2D de individuos (población), shape=(poblacion, n).
        flow (numpy.ndarray): Matriz de flujos, shape=(n, n).
        distances (numpy.ndarray): Matriz de distancias, shape=(n, n).

    Returns:
        numpy.ndarray: Array de fitness para cada individuo, shape=(poblacion,).
    """
    try:
        # population: shape=(poblacion, n)
        # flow: shape=(n, n)
        # distances: shape=(n, n)

        # Expand dimensions to perform broadcasting
        # flow[np.newaxis, :, :] -> shape=(1, n, n)
        # population[:, :, np.newaxis] -> shape=(poblacion, n, 1)
        # population[:, np.newaxis, :] -> shape=(poblacion, 1, n)
        # distances[population[:, :, np.newaxis], population[:, np.newaxis, :]] -> shape=(poblacion, n, n)

        fitness = np.sum(flow[np.newaxis, :, :] * distances[population[:, :, np.newaxis], population[:, np.newaxis, :]], axis=(1, 2))
        return fitness
    except Exception as e:
        logging.error(f"Error al calcular el fitness de la población: {e}")
        raise