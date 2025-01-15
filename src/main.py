# src/main.py

import argparse
import logging
import os
import sys
import random
import json
import numpy as np

from src.genetic_algorithm import ejecutar_algoritmo_genetico
from src.baldwinian_ga import ejecutar_varianta_baldwiniana
from src.lamarckian_ga import ejecutar_varianta_lamarckiana
from src.utils import cargar_datos
from src.plotting import graficar_historial, graficar_comparativa


def configurar_logging(ruta_salida):
    """
    Configura el sistema de logging.

    Args:
        ruta_salida (str): Directorio donde se guardarán los logs.
    """
    log_file = os.path.join(ruta_salida, 'ejecucion.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def guardar_resultados(mejor_solucion, ruta_salida):
    """
    Guarda la mejor solución encontrada en un archivo de texto.

    Args:
        mejor_solucion (tuple): Tupla que contiene la permutación y el coste.
        ruta_salida (str): Directorio donde se guardará el archivo.
    """
    archivo_resultado = os.path.join(ruta_salida, 'mejor_solucion.txt')
    try:
        with open(archivo_resultado, 'w', encoding='utf-8') as f:
            f.write(f"Coste de la mejor solución: {mejor_solucion[1]}\n")
            f.write("Permutación: " + ' '.join(map(str, mejor_solucion[0])) + "\n")
        logging.info(f"Mejor solución guardada en {archivo_resultado}")
    except Exception as e:
        logging.error(f"Error al guardar la mejor solución: {e}")


def guardar_historial(historial, ruta_salida, variant):
    """
    Guarda el historial de fitness en un archivo JSON.

    Args:
        historial (list o numpy.ndarray): Lista de valores de fitness por generación.
        ruta_salida (str): Directorio donde se guardará el archivo.
        variant (str): Nombre de la variante del Algoritmo Genético.
    """
    archivo_historial = os.path.join(ruta_salida, f'historial_fitness_{variant}.json')
    try:
        with open(archivo_historial, 'w', encoding='utf-8') as f:
            json.dump(historial, f, indent=4)
        logging.info(f"Historial de fitness guardado en {archivo_historial}")
    except Exception as e:
        logging.error(f"Error al guardar el historial de fitness: {e}")


def fijar_semilla(seed):
    """
    Fija la semilla para los generadores de números aleatorios.

    Args:
        seed (int): Valor de la semilla.
    """
    random.seed(seed)
    np.random.seed(seed)
    logging.info(f"Semilla fijada en: {seed}")


def main():
    # Definir argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Algoritmos Genéticos para el Problema de Asignación Cuadrática (QAP)')
    parser.add_argument('--variant', type=str, required=True,
                        choices=['standard', 'baldwinian', 'lamarckian'],
                        help='Variante del Algoritmo Genético a ejecutar')
    parser.add_argument('--data', type=str, required=True,
                        help='Ruta al archivo de datos (e.g., data/raw/tai256c.dat)')
    parser.add_argument('--output', type=str, required=True,
                        help='Directorio donde se guardarán los resultados')

    # Opcionales: Parámetros del Algoritmo Genético
    parser.add_argument('--population', type=int, default=100,
                        help='Tamaño de la población')
    parser.add_argument('--generations', type=int, default=500,
                        help='Número de generaciones')
    parser.add_argument('--crossover_rate', type=float, default=0.8,
                        help='Tasa de cruce')
    parser.add_argument('--mutation_rate', type=float, default=0.02,
                        help='Tasa de mutación')
    parser.add_argument('--elitismo', action='store_true',
                        help='Activar elitismo')
    parser.add_argument('--seed', type=int, default=None,
                        help='Semilla para los generadores de números aleatorios')

    args = parser.parse_args()

    # Crear directorio de salida si no existe
    os.makedirs(args.output, exist_ok=True)

    # Configurar logging
    configurar_logging(args.output)
    logging.info("Inicio de la ejecución del Algoritmo Genético")

    # Fijar la semilla si se proporcionó
    if args.seed is not None:
        fijar_semilla(args.seed)
    else:
        # Opcional: fijar una semilla predeterminada o dejarla aleatoria
        logging.info("No se proporcionó semilla. Usando una semilla aleatoria.")

    # Cargar datos
    try:
        n, flow_matrix, distance_matrix = cargar_datos(args.data)
        logging.info(f"Datos cargados correctamente desde {args.data}")
        logging.info(f"Número de instalaciones/localizaciones: {n}")
    except Exception as e:
        logging.error(f"Error al cargar los datos: {e}")
        sys.exit(1)

    # Definir parámetros del Algoritmo Genético
    parametros = {
        'poblacion': args.population,
        'generaciones': args.generations,
        'tasa_cruce': args.crossover_rate,
        'tasa_mutacion': args.mutation_rate,
        'elitismo': args.elitismo
    }

    # Ejecutar la variante seleccionada
    try:
        if args.variant == 'standard':
            mejor_solucion, historial = ejecutar_algoritmo_genetico(n, flow_matrix, distance_matrix, parametros)
            logging.info("Algoritmo Genético Estándar ejecutado con éxito.")
        elif args.variant == 'baldwinian':
            mejor_solucion, historial = ejecutar_varianta_baldwiniana(n, flow_matrix, distance_matrix, parametros)
            logging.info("Variante Baldwiniana ejecutada con éxito.")
        elif args.variant == 'lamarckian':
            mejor_solucion, historial = ejecutar_varianta_lamarckiana(n, flow_matrix, distance_matrix, parametros)
            logging.info("Variante Lamarckiana ejecutada con éxito.")
    except Exception as e:
        logging.error(f"Error durante la ejecución de la variante {args.variant}: {e}")
        sys.exit(1)

    # Guardar resultados
    guardar_resultados(mejor_solucion, args.output)

    # Guardar historial de fitness
    guardar_historial(historial, args.output, variant=args.variant)

    # Graficar historial de fitness
    try:
        graficar_historial(historial, args.output, variant=args.variant)
        logging.info("Historial de fitness graficado correctamente.")
    except Exception as e:
        logging.error(f"Error al graficar el historial de fitness: {e}")

    logging.info("Ejecución finalizada exitosamente.")


if __name__ == "__main__":
    main()
