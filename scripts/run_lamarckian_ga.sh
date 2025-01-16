#!/bin/bash

# scripts/run_lamarckian_ga.sh

# Descripción:
# Ejecuta la Variante Lamarckiana del Algoritmo Genético para el QAP usando el archivo de datos tai256c.dat.
# Los resultados se guardarán en el directorio results/lamarckian_ga/

# Activar entorno virtual si lo estás utilizando
# source ../venv/bin/activate

echo "Ejecutando Variante Lamarckiana del Algoritmo Genético..."

python src/main.py --variant lamarckian \
                   --data data/raw/tai256c.dat \
                   --output results/lamarckian_ga/

echo "Variante Lamarckiana del Algoritmo Genético finalizada."