# src/utils.py

import numpy as np
import os
import logging


def cargar_datos(ruta_archivo):
    """
    Carga los datos del archivo especificado.

    El archivo debe tener el siguiente formato:
    n
    A (matriz de flujos) - n líneas de n enteros
    B (matriz de distancias) - n líneas de n números (pueden ser flotantes)

    Args:
        ruta_archivo (str): Ruta al archivo de datos.

    Returns:
        tuple: Número de instalaciones, matriz de flujos (int32), matriz de distancias (float32).
    """
    try:
        # Verificar si el archivo existe
        if not os.path.isfile(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")

        # Cargar todos los datos excepto la primera línea (n)
        data = np.loadtxt(ruta_archivo, skiprows=1)

        # Verificar que hay 2n líneas después de la primera línea
        n = int(data.shape[0] / 2)
        if data.shape[0] != 2 * n or data.shape[1] != n:
            raise ValueError(f"El archivo {ruta_archivo} no tiene las dimensiones esperadas.")

        # Separar las matrices de flujo y distancia
        flow = np.int32(data[:n, :])
        distances = np.float32(data[n:, :])

        return n, flow, distances

    except Exception as e:
        logging.error(f"Error al cargar los datos desde {ruta_archivo}: {e}")
        raise
    
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
    logging.debug(f"Flujo total por instalación: {flujo_total}")

    # Calcular la distancia total para cada ubicación (suma de filas)
    distancia_total = np.sum(distancia_matrix, axis=1)
    logging.debug(f"Distancia total por ubicación: {distancia_total}")

    # Ordenar instalaciones por flujo total descendente
    instalaciones_ordenadas = np.argsort(-flujo_total)
    logging.debug(f"Instalaciones ordenadas (descendente por flujo): {instalaciones_ordenadas}")

    # Ordenar ubicaciones por distancia total ascendente
    ubicaciones_ordenadas = np.argsort(distancia_total)
    logging.debug(f"Ubicaciones ordenadas (ascendente por distancia): {ubicaciones_ordenadas}")

    # Asignar instalaciones a ubicaciones
    asignacion = np.empty(n, dtype=int)
    for i in range(n):
        asignacion[ubicaciones_ordenadas[i]] = instalaciones_ordenadas[i]
        logging.debug(f"Asignando instalación {instalaciones_ordenadas[i]} a ubicación {ubicaciones_ordenadas[i]}")

    return asignacion