# scripts/run_baldwinian_ga.ps1

# Descripción:
# Ejecuta la Variante Baldwiniana del Algoritmo Genético para el QAP utilizando el archivo de datos tai256c.dat.
# Los resultados se guardarán en el directorio results/baldwinian_ga/

function Handle-Error {
    param([string]$message)
    Write-Error $message
    exit 1
}

# Definir variables
$Variant = "baldwinian"
$DataFile = "data/raw/tai256c.dat"
$OutputDir = "results/baldwinian_ga/"
$Population = 100
$Generations = 500
$CrossoverRate = 0.8
$MutationRate = 0.02
$Elitismo = $true

# Crear el directorio de salida si no existe
New-Item -ItemType Directory -Path $OutputDir -Force

# Activar entorno virtual
try {
    & "venv\Scripts\Activate.ps1" -ErrorAction Stop
} catch {
    Handle-Error "No se pudo activar el entorno virtual."
}

Write-Host "===== Inicio de la Variante Baldwiniana del Algoritmo Genético ====="

# Ejecutar el script principal con los parámetros adecuados
try {
    python src/main.py `
        --variant $Variant `
        --data $DataFile `
        --output $OutputDir `
        --population $Population `
        --generations $Generations `
        --crossover_rate $CrossoverRate `
        --mutation_rate $MutationRate `
        --elitismo
} catch {
    Handle-Error "Variante Baldwiniana falló."
}

Write-Host "===== Fin de la Variante Baldwiniana del Algoritmo Genético ====="
Write-Host "Resultados guardados en $OutputDir"

# Desactivar entorno virtual
deactivate
