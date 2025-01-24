import numpy as np
import random
from src.fitness import fitness_pop
from src.selection import seleccion_torneo
from src.crossover import cruce_pmx
from src.mutation import mutacion_swap
from src.optimization import optimizar_individuo_busqueda_local, generar_poblacion

def ejecutar_varianta_lamarckiana(n, flujo_matrix, distancia_matrix, parametros=None):
    """
    Ejecuta la Variante Lamarckiana del Algoritmo Genético para el QAP utilizando Búsqueda Local con máscara booleana para la evaluación del fitness.

    En la variante Lamarckiana, las mejoras realizadas durante la búsqueda local se incorporan directamente en los individuos de la población,
    lo que significa que la información aprendida se transmite a la población genética.

    Args:
        n (int): Número de instalaciones/localizaciones.
        flujo_matrix (numpy.ndarray): Matriz de flujos.
        distancia_matrix (numpy.ndarray): Matriz de distancias.
        parametros (dict, optional): Parámetros del Algoritmo Genético y Búsqueda Local.

    Returns:
        tuple: Mejor solución encontrada y su historial de fitness.
    """
    if parametros is None:
        parametros = {
            'poblacion': 100,
            'generaciones': 500,
            'tasa_cruce': 0.8,
            'tasa_mutacion': 0.02,
            'elitismo': True,
            'tam_poblacion_opt': 50,  # Tamaño de la población a optimizar
            'hill_climbing_max_iter': 1000
        }

    # Inicializar población
    print("Generando población inicial...")
    poblacion = generar_poblacion(parametros['poblacion'], n, seed=196917)

    # Verificar la validez de la población
    print("Verificando la validez de la población inicial...")
    for idx, ind in enumerate(poblacion):
        assert set(ind) == set(range(n)), f"El individuo {idx} no es una permutación válida."

    # Aplicar optimización local a una parte de la población inicial
    print("Aplicando búsqueda local a la población inicial...")
    indices_opt = np.random.choice(len(poblacion), parametros['tam_poblacion_opt'], replace=False)
    for idx in indices_opt:
        poblacion[idx], _ = optimizar_individuo_busqueda_local(
            poblacion[idx], flujo_matrix, distancia_matrix, max_iter=parametros['hill_climbing_max_iter']
        )

    fitness = fitness_pop(poblacion, flujo_matrix, distancia_matrix)

    # Inicializar historial y encontrar la mejor solución inicial
    historial = []
    mejor_idx = np.argmin(fitness)
    mejor_solucion = (poblacion[mejor_idx], fitness[mejor_idx])
    historial.append(mejor_solucion[1])

    print(f"Generación 0: Mejor fitness = {mejor_solucion[1]}")

    for gen in range(parametros['generaciones']):
        nueva_poblacion = []

        # Elitismo: mantener el mejor individuo
        if parametros['elitismo']:
            nueva_poblacion.append(poblacion[mejor_idx].copy())

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

            # Verificar que los hijos son permutaciones válidas
            #assert set(hijo1) == set(range(n)), "Hijo1 no es una permutación válida después de mutación."
            #assert set(hijo2) == set(range(n)), "Hijo2 no es una permutación válida después de mutación."

            # Aplicar optimización local a los hijos (Lamarckiano: incorporar aprendizaje)
            hijo1, _ = optimizar_individuo_busqueda_local(
                hijo1, flujo_matrix, distancia_matrix, max_iter=parametros['hill_climbing_max_iter']
            )
            hijo2, _ = optimizar_individuo_busqueda_local(
                hijo2, flujo_matrix, distancia_matrix, max_iter=parametros['hill_climbing_max_iter']
            )

            nueva_poblacion.extend([hijo1, hijo2])

        # Convertir a array de NumPy y truncar si es necesario
        poblacion = np.array(nueva_poblacion[:parametros['poblacion']])

        # Verificar la validez de la nueva población
        #for idx, ind in enumerate(poblacion):
            #assert set(ind) == set(range(n)), f"El individuo {idx} no es una permutación válida."

        # Aplicar optimización local a una parte de la nueva población
        indices_opt = np.random.choice(len(poblacion), parametros['tam_poblacion_opt'], replace=False)
        for idx in indices_opt:
            poblacion[idx], _ = optimizar_individuo_busqueda_local(
                poblacion[idx], flujo_matrix, distancia_matrix, max_iter=parametros['hill_climbing_max_iter']
            )

        fitness = fitness_pop(poblacion, flujo_matrix, distancia_matrix)

        # Actualizar el mejor individuo
        mejor_idx = np.argmin(fitness)
        mejor_gen = (poblacion[mejor_idx], fitness[mejor_idx])
        historial.append(mejor_gen[1])

        if mejor_gen[1] < mejor_solucion[1]:
            mejor_solucion = mejor_gen

        # Imprimir progreso cada 100 generaciones y al inicio
        if (gen + 1) % 100 == 0 or gen == 0:
            print(f"Generación {gen + 1}: Mejor fitness = {mejor_solucion[1]}")

    return mejor_solucion, historial
