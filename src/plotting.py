# src/plotting.py

import matplotlib.pyplot as plt
import os

def graficar_historial(historial, ruta_salida, variant):
    """
    Genera y guarda una gráfica del historial de fitness a lo largo de las generaciones.
    
    Args:
        historial (list o numpy.ndarray): Lista de valores de fitness por generación.
        ruta_salida (str): Directorio donde se guardará la gráfica.
        variant (str): Nombre de la variante del Algoritmo Genético (e.g., 'standard').
    """
    plt.figure(figsize=(10, 6))
    plt.plot(historial, marker='o', linestyle='-', color='b', label='Fitness')
    plt.title(f'Historial de Fitness - Variante {variant.capitalize()}')
    plt.xlabel('Generación')
    plt.ylabel('Fitness (Coste)')
    plt.grid(True)
    plt.legend()
    
    # Asegurarse de que la ruta de salida exista
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    
    # Definir el nombre del archivo
    nombre_archivo = f'historial_fitness_{variant}.png'
    ruta_completa = os.path.join(ruta_salida, nombre_archivo)
    
    # Guardar la gráfica
    plt.savefig(ruta_completa, dpi=300, bbox_inches='tight')
    plt.close()

def graficar_comparativa(historial_variantes, ruta_salida):
    """
    Genera y guarda una gráfica comparativa del historial de fitness para múltiples variantes.
    
    Args:
        historial_variantes (dict): Diccionario donde las llaves son los nombres de las variantes
                                     y los valores son las listas de fitness por generación.
        ruta_salida (str): Directorio donde se guardará la gráfica.
    """
    plt.figure(figsize=(12, 8))
    
    for variant, historial in historial_variantes.items():
        plt.plot(historial, marker='o', linestyle='-', label=variant.capitalize())
    
    plt.title('Comparativa de Historial de Fitness entre Variantes del Algoritmo Genético')
    plt.xlabel('Generación')
    plt.ylabel('Fitness (Coste)')
    plt.grid(True)
    plt.legend()
    
    # Asegurarse de que la ruta de salida exista
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    
    # Definir el nombre del archivo
    nombre_archivo = 'comparativa_historial_fitness.png'
    ruta_completa = os.path.join(ruta_salida, nombre_archivo)
    
    # Guardar la gráfica
    plt.savefig(ruta_completa, dpi=300, bbox_inches='tight')
    plt.close()