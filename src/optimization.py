import numpy as np
import multiprocessing as mp
from numba import njit
from src.fitness import fitness_pop, calcular_coste

@njit
def calcular_delta_coste_numba(individuo, flujo_matrix, distancia_matrix, r, s):
    """
    Calcula la diferencia de coste al intercambiar dos posiciones en la permutación.

    Args:
        individuo (np.ndarray): Permutación actual.
        flujo_matrix (np.ndarray): Matriz de flujos.
        distancia_matrix (np.ndarray): Matriz de distancias.
        r (int): Índice de la primera posición a intercambiar.
        s (int): Índice de la segunda posición a intercambiar.

    Returns:
        float: Diferencia en el coste tras el intercambio.
    """
    delta = 0.0
    n = individuo.shape[0]

    p_r, p_s = individuo[r], individuo[s]

    for k in range(n):
        if k != r and k != s:
            p_k = individuo[k]
            delta += (
                flujo_matrix[r, k] * (distancia_matrix[p_s, p_k] - distancia_matrix[p_r, p_k]) +
                flujo_matrix[s, k] * (distancia_matrix[p_r, p_k] - distancia_matrix[p_s, p_k]) +
                flujo_matrix[k, r] * (distancia_matrix[p_k, p_s] - distancia_matrix[p_k, p_r]) +
                flujo_matrix[k, s] * (distancia_matrix[p_k, p_r] - distancia_matrix[p_k, p_s])
            )
    return delta

@njit
def actualizar_coste_incremental(coste_actual, flujo_matrix, distancia_matrix, individuo, r, s):
    """
    Actualiza el coste total de manera incremental tras un intercambio.

    Args:
        coste_actual (float): Coste total antes del intercambio.
        flujo_matrix (np.ndarray): Matriz de flujos.
        distancia_matrix (np.ndarray): Matriz de distancias.
        individuo (np.ndarray): Permutación actual.
        r (int): Índice de la primera posición intercambiada.
        s (int): Índice de la segunda posición intercambiada.

    Returns:
        float: Nuevo coste total tras el intercambio.
    """
    delta = calcular_delta_coste_numba(individuo, flujo_matrix, distancia_matrix, r, s)
    return coste_actual + delta

def mejor_vecino_con_mascara(individuo, flujo_matrix, distancia_matrix, mascara, mascara_permutacion, coste_actual, max_vecinos=100):
    """
    Encuentra el mejor vecino evitando combinaciones ya probadas usando una máscara booleana
    y limitando el número de vecinos evaluados a un subconjunto aleatorio.

    Args:
        individuo (np.ndarray): Permutación actual.
        flujo_matrix (np.ndarray): Matriz de flujos.
        distancia_matrix (np.ndarray): Matriz de distancias.
        mascara (np.ndarray): Matriz booleana que indica combinaciones prohibidas.
        mascara_permutacion (np.ndarray): Máscara 1D para índices bloqueados.
        coste_actual (float): Coste actual del individuo.
        max_vecinos (int): Número máximo de vecinos a evaluar.

    Returns:
        tuple: (nueva permutación, nuevo coste, nueva máscara, nueva máscara_permutacion)
    """
    n = len(individuo)
    mejor_delta = 0.0
    mejor_swap = None

    # Generar un subconjunto aleatorio de pares (r, s)
    vecinos = [(r, s) for r in range(n) for s in range(r + 1, n) if not mascara[r, s]]
    np.random.shuffle(vecinos)
    vecinos = vecinos[:max_vecinos]  # Limitar a max_vecinos

    for r, s in vecinos:
        if not mascara_permutacion[r] or not mascara_permutacion[s]:
            continue

        delta = calcular_delta_coste_numba(individuo, flujo_matrix, distancia_matrix, r, s)
        if delta < mejor_delta:
            mejor_delta = delta
            mejor_swap = (r, s)

    if mejor_swap:
        r, s = mejor_swap
        nuevo_individuo = individuo.copy()
        nuevo_individuo[r], nuevo_individuo[s] = nuevo_individuo[s], nuevo_individuo[r]
        nuevo_coste = actualizar_coste_incremental(coste_actual, flujo_matrix, distancia_matrix, individuo, r, s)
        mascara[r, s] = True  # Marcar la combinación como probada

        # Reactivar los índices afectados
        mascara_permutacion[r] = True
        mascara_permutacion[s] = True
        return nuevo_individuo, nuevo_coste, mascara, mascara_permutacion
    else:
        # Bloquear los índices si no hay mejoras
        for i in range(n):
            mascara_permutacion[i] = False
        return individuo, coste_actual, mascara, mascara_permutacion

def calcula_busqueda_local_con_mascara(individuo, flujo_matrix, distancia_matrix, max_iter=50000, max_vecinos=100):
    """
    Realiza una búsqueda local con una máscara booleana para evitar probar combinaciones repetidas
    y una máscara de exclusión para la permutación.

    Args:
        individuo (np.ndarray): Permutación inicial.
        flujo_matrix (np.ndarray): Matriz de flujos.
        distancia_matrix (np.ndarray): Matriz de distancias.
        max_iter (int): Número máximo de iteraciones.
        max_vecinos (int): Número máximo de vecinos a evaluar por iteración.

    Returns:
        tuple: (mejor permutación encontrada, coste asociado)
    """
    n = len(individuo)
    mejor_individuo = individuo.copy()
    mejor_coste = calcular_coste(mejor_individuo, flujo_matrix, distancia_matrix)

    # Inicializa las máscaras
    mascara = np.zeros((n, n), dtype=bool)
    mascara_permutacion = np.ones(n, dtype=bool)  # Todos los índices inicialmente desbloqueados

    for _ in range(max_iter):
        nuevo_individuo, nuevo_coste, mascara, mascara_permutacion = mejor_vecino_con_mascara(
            mejor_individuo, flujo_matrix, distancia_matrix, mascara, mascara_permutacion, mejor_coste, max_vecinos
        )

        if nuevo_coste < mejor_coste:  # Si hay mejora, actualizar
            mejor_individuo = nuevo_individuo
            mejor_coste = nuevo_coste
        else:  # Si no hay mejoras, detener
            break

    return mejor_individuo, mejor_coste

def optimizar_individuo_busqueda_local(individuo, flujo_matrix, distancia_matrix, max_iter=50000, max_vecinos=100):
    """
    Aplica la optimización local a un único individuo utilizando búsqueda local con máscara booleana.

    Args:
        individuo (np.ndarray): Individuo a optimizar.
        flujo_matrix (np.ndarray): Matriz de flujos.
        distancia_matrix (np.ndarray): Matriz de distancias.
        max_iter (int): Número máximo de iteraciones para la búsqueda local.
        max_vecinos (int): Número máximo de vecinos a evaluar por iteración.

    Returns:
        tuple: (Individuo optimizado, coste asociado)
    """
    return calcula_busqueda_local_con_mascara(individuo, flujo_matrix, distancia_matrix, max_iter, max_vecinos)

def generar_individuo(n, seed=None):
    """
    Genera un individuo aleatorio para la población.

    Args:
        n (int): Número de instalaciones/localizaciones.
        seed (int, optional): Semilla para reproducibilidad.

    Returns:
        np.ndarray: Permutación aleatoria de asignaciones.
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.permutation(n)

def generar_poblacion(tam_poblacion, n, seed=None):
    """
    Genera una población de individuos aleatorios.

    Args:
        tam_poblacion (int): Tamaño de la población.
        n (int): Número de instalaciones/localizaciones.
        seed (int, optional): Semilla para reproducibilidad.

    Returns:
        np.ndarray: Población de individuos.
    """
    if seed is not None:
        np.random.seed(seed)
    return np.array([np.random.permutation(n) for _ in range(tam_poblacion)])
