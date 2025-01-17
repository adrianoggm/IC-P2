# src/genetic_algorithm.py

import numpy as np
import random
from src.fitness import fitness_pop, calcular_coste
from src.selection import seleccion_torneo
from src.crossover import cruce_pmx
from src.mutation import mutacion_swap
from src.optimization import optimizacion_2opt

def ejecutar_algoritmo_genetico(n, flujo_matrix, distancia_matrix, parametros=None):
    """
    Ejecuta el Algoritmo Genético Estándar para el QAP.

    Args:
        n (int): Número de instalaciones/localizaciones.
        flujo_matrix (numpy.ndarray): Matriz de flujos, shape=(n, n).
        distancia_matrix (numpy.ndarray): Matriz de distancias, shape=(n, n).
        parametros (dict, optional): Parámetros del Algoritmo Genético.

    Returns:
        tuple: Mejor solución encontrada (individuo, coste) y su historial de fitness.
    """
    if parametros is None:
        parametros = {
            'poblacion': 100,
            'generaciones': 500,
            'tasa_cruce': 0.8,
            'tasa_mutacion': 0.02,
            'elitismo': True
        }

    print("Inicializando población")
    poblacion = []
    mitad_poblacion = parametros['poblacion'] // 2

    # Generar la primera mitad de la población de forma aleatoria
    for _ in range(mitad_poblacion):
        individuo = generar_individuo(n)
        poblacion.append(individuo)

    # Generar la segunda mitad de la población usando la heurística greedy
    for _ in range(parametros['poblacion'] - mitad_poblacion):
        individuo = generar_individuo_greedy(n, flujo_matrix, distancia_matrix)
        poblacion.append(individuo)

    poblacion = np.array(poblacion)
    fitness = fitness_pop(poblacion, flujo_matrix, distancia_matrix)

    historial = []
    mejor_idx = np.argmin(fitness)
    mejor_solucion = (poblacion[mejor_idx], fitness[mejor_idx])
    historial.append(mejor_solucion[1])
    print(f"Generación 0: Mejor fitness = {mejor_solucion[1]}")

    for gen in range(parametros['generaciones']):
        nueva_poblacion = []

        # Elitismo: mantener el mejor individuo
        if parametros['elitismo']:
            nueva_poblacion.append(mejor_solucion[0].copy())

        while len(nueva_poblacion) < parametros['poblacion']:
            # Selección
            padre1 = seleccion_torneo(poblacion, fitness)
            padre2 = seleccion_torneo(poblacion, fitness)

            # Cruce
            if random.random() < parametros['tasa_cruce']:
                hijo1, hijo2 = cruce_pmx(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()

            # Mutación
            hijo1 = mutacion_swap(hijo1, parametros['tasa_mutacion'])
            hijo2 = mutacion_swap(hijo2, parametros['tasa_mutacion'])

            # Añadir los hijos a la nueva población
            nueva_poblacion.extend([hijo1, hijo2])

        # Convertir a array de NumPy y truncar si es necesario
        poblacion = np.array(nueva_poblacion[:parametros['poblacion']])
        fitness = fitness_pop(poblacion, flujo_matrix, distancia_matrix)

        # Actualizar el mejor individuo
        mejor_idx = np.argmin(fitness)
        mejor_gen = (poblacion[mejor_idx], fitness[mejor_idx])
        historial.append(mejor_gen[1])

        if mejor_gen[1] < mejor_solucion[1]:
            mejor_solucion = mejor_gen

        # Imprimir progreso cada 100 generaciones y en la primera generación
        if (gen + 1) % 100 == 0 or gen == 0:
            print(f"Generación {gen + 1}: Mejor fitness = {mejor_solucion[1]}")

    return mejor_solucion, historial

def generar_individuo(n):
    """
    Genera un individuo aleatorio para la población.

    Args:
        n (int): Número de instalaciones/localizaciones.

    Returns:
        numpy.ndarray: Permutación aleatoria de asignaciones, shape=(n,).
    """
    individuo = np.arange(n)
    np.random.shuffle(individuo)
    return individuo

def generar_individuo_greedy(n, flujo_matrix, distancia_matrix):
    """
    Genera un individuo utilizando una heurística greedy.
    Asigna las instalaciones con mayor flujo total a las ubicaciones con menor distancia total.

    Args:
        n (int): Número de instalaciones/localizaciones.
        flujo_matrix (numpy.ndarray): Matriz de flujos, shape=(n, n).
        distancia_matrix (numpy.ndarray): Matriz de distancias, shape=(n, n).

    Returns:
        numpy.ndarray: Permutación resultante de la heurística greedy, shape=(n,).
    """
    # Calcular el flujo total para cada instalación (suma de filas)
    flujo_total = np.sum(flujo_matrix, axis=1)

    # Calcular la distancia total para cada ubicación (suma de filas)
    distancia_total = np.sum(distancia_matrix, axis=1)

    # Ordenar instalaciones por flujo total descendente
    instalaciones_ordenadas = np.argsort(-flujo_total)

    # Ordenar ubicaciones por distancia total ascendente
    ubicaciones_ordenadas = np.argsort(distancia_total)

    # Asignar instalaciones a ubicaciones
    asignacion = np.empty(n, dtype=int)
    for i in range(n):
        asignacion[ubicaciones_ordenadas[i]] = instalaciones_ordenadas[i]

    return asignacion
