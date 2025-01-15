#!/bin/bash

# scripts/run_standard_ga.sh

# Descripción:
# Ejecuta el Algoritmo Genético Estándar para el QAP usando el archivo de datos tai256c.dat.
# Los resultados se guardarán en el directorio results/standard_ga/

# Activar entorno virtual si lo estás utilizando
# source ../venv/bin/activate

echo "Ejecutando Algoritmo Genético Estándar..."

python src/main.py --variant standard \
                   --data data/raw/tai256c.dat \
                   --output results/standard_ga/

echo "Algoritmo Genético Estándar finalizado."