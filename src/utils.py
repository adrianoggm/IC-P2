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