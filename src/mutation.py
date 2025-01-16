# src/mutation.py

import numpy as np
import random

def mutacion_swap(individuo, tasa_mutacion):
    """
    Realiza una mutación de intercambio en el individuo con una cierta probabilidad.

    Args:
        individuo (list o numpy.ndarray): Individuo a mutar, shape=(n,).
        tasa_mutacion (float): Probabilidad de que ocurra una mutación.

    Returns:
        numpy.ndarray: Individuo mutado.
    """
    individuo_mutado = individuo.copy()
    if random.random() < tasa_mutacion:
        i, j = random.sample(range(len(individuo)), 2)
        individuo_mutado[i], individuo_mutado[j] = individuo_mutado[j], individuo_mutado[i]
    return individuo_mutado