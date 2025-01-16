# src/lamarckian_ga.py

import numpy as np
import random
from src.fitness import fitness_pop, calcular_coste
from src.selection import seleccion_torneo
from src.crossover import cruce_pmx
from src.mutation import mutacion_swap
from src.optimization import optimizacion_2opt


def ejecutar_varianta_lamarckiana(n, flujo_matrix, distancia_matrix, parametros=None):
    """
    Ejecuta la Variante Lamarckiana del Algoritmo Genético para el QAP.

    Args:
        n (int): Número de instalaciones/localizaciones.
        flujo_matrix (numpy.ndarray): Matriz de flujos.
        distancia_matrix (numpy.ndarray): Matriz de distancias.
        parametros (dict, optional): Parámetros del Algoritmo Genético.

    Returns:
        tuple: Mejor solución encontrada y su historial de fitness.
    """
    if parametros is None:
        parametros = {
            'poblacion': 100,
            'generaciones': 500,
            'tasa_cruce': 0.8,
            'tasa_mutacion': 0.02,
            'elitismo': True
        }

    # Inicializar población como un array de NumPy
    poblacion = np.array([generar_individuo(n) for _ in range(parametros['poblacion'])])
    # Aplicar optimización local a cada individuo y actualizar la población
    poblacion_mejorada = np.array([optimizar_individuo(ind, flujo_matrix, distancia_matrix) for ind in poblacion])
    fitness = fitness_pop(poblacion_mejorada, flujo_matrix, distancia_matrix)

    historial = []
    mejor_idx = np.argmin(fitness)
    mejor_solucion = (poblacion_mejorada[mejor_idx], fitness[mejor_idx])
    historial.append(mejor_solucion[1])

    for gen in range(parametros['generaciones']):
        nueva_poblacion = []

        # Elitismo: mantener el mejor individuo
        if parametros['elitismo']:
            nueva_poblacion.append(mejor_solucion[0])

        while len(nueva_poblacion) < parametros['poblacion']:
            # Selección
            padre1 = seleccion_torneo(poblacion_mejorada, fitness)
            padre2 = seleccion_torneo(poblacion_mejorada, fitness)

            # Cruce
            if random.random() < parametros['tasa_cruce']:
                hijo1, hijo2 = cruce_pmx(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()

            # Mutación
            hijo1 = mutacion_swap(hijo1, parametros['tasa_mutacion'])
            hijo2 = mutacion_swap(hijo2, parametros['tasa_mutacion'])

            # Optimización Local y actualización de la población
            hijo1_mejorado, _ = optimizacion_2opt(hijo1, flujo_matrix, distancia_matrix)
            hijo2_mejorado, _ = optimizacion_2opt(hijo2, flujo_matrix, distancia_matrix)

            nueva_poblacion.extend([hijo1_mejorado, hijo2_mejorado])

        # Convertir a array de NumPy y truncar si es necesario
        poblacion = np.array(nueva_poblacion[:parametros['poblacion']])
        # Calcular fitness de la nueva población
        poblacion_mejorada = poblacion.copy()
        fitness = fitness_pop(poblacion_mejorada, flujo_matrix, distancia_matrix)

        # Actualizar el mejor individuo
        mejor_idx = np.argmin(fitness)
        mejor_gen = (poblacion_mejorada[mejor_idx], fitness[mejor_idx])
        historial.append(mejor_gen[1])

        if mejor_gen[1] < mejor_solucion[1]:
            mejor_solucion = mejor_gen

        # Opcional: Imprimir progreso
        if (gen + 1) % 100 == 0 or gen == 0:
            print(f"Generación {gen + 1}: Mejor fitness = {mejor_solucion[1]}")

    return mejor_solucion, historial


def generar_individuo(n):
    """
    Genera un individuo aleatorio para la población.

    Args:
        n (int): Número de instalaciones/localizaciones.

    Returns:
        numpy.ndarray: Permutación aleatoria de asignaciones.
    """
    individuo = np.arange(n)
    np.random.shuffle(individuo)
    return individuo


def optimizar_individuo(individuo, flujo_matrix, distancia_matrix):
    """
    Aplica la optimización local 2-opt a un individuo.

    Args:
        individuo (numpy.ndarray): Individuo a optimizar.
        flujo_matrix (numpy.ndarray): Matriz de flujos.
        distancia_matrix (numpy.ndarray): Matriz de distancias.

    Returns:
        tuple: Individuo optimizado y su coste.
    """
    optimizado, coste = optimizacion_2opt(individuo, flujo_matrix, distancia_matrix)
    return optimizado, coste
