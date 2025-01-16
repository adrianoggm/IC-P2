#!/bin/bash

# scripts/run_all.sh

# Descripción:
# Ejecuta todas las variantes del Algoritmo Genético secuencialmente.
# Primero ejecuta el Algoritmo Genético Estándar, luego la Variante Baldwiniana y finalmente la Variante Lamarckiana.
# Los resultados se guardarán en los respectivos directorios dentro de results/

# Activar entorno virtual si lo estás utilizando
# source ../venv/bin/activate

echo "Iniciando ejecución de todas las variantes del Algoritmo Genético..."

# Ejecutar Algoritmo Genético Estándar
bash scripts/run_standard_ga.sh

# Verificar si el anterior script finalizó correctamente
if [ $? -ne 0 ]; then
    echo "Error al ejecutar el Algoritmo Genético Estándar. Abortando ejecución."
    exit 1
fi

# Ejecutar Variante Baldwiniana
bash scripts/run_baldwinian_ga.sh

# Verificar si el anterior script finalizó correctamente
if [ $? -ne 0 ]; then
    echo "Error al ejecutar la Variante Baldwiniana. Abortando ejecución."
    exit 1
fi

# Ejecutar Variante Lamarckiana
bash scripts/run_lamarckian_ga.sh

# Verificar si el anterior script finalizó correctamente
if [ $? -ne 0 ]; then
    echo "Error al ejecutar la Variante Lamarckiana. Abortando ejecución."
    exit 1
fi

echo "Todas las variantes del Algoritmo Genético han finalizado correctamente."
