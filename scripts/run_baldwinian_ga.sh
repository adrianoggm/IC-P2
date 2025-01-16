#!/bin/bash

# scripts/run_baldwinian_ga.sh

# Descripción:
# Ejecuta la Variante Baldwiniana del Algoritmo Genético para el QAP usando el archivo de datos tai256c.dat.
# Los resultados se guardarán en el directorio results/baldwinian_ga/

# Activar entorno virtual si lo estás utilizando
# source ../venv/bin/activate

echo "Ejecutando Variante Baldwiniana del Algoritmo Genético..."

python src/main.py --variant baldwinian \
                   --data data/raw/tai256c.dat \
                   --output results/baldwinian_ga/

echo "Variante Baldwiniana del Algoritmo Genético finalizada."