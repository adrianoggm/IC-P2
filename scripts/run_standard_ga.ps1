# scripts/run_standard_ga.ps1

# Descripción:
# Ejecuta el Algoritmo Genético Estándar para el QAP utilizando el archivo de datos tai256c.dat.
# Los resultados se guardarán en el directorio results/standard_ga/
# Puedes especificar una semilla opcional.

function Handle-Error {
    param([string]$message)
    Write-Error $message
    exit 1
}

# Definir variables
$Variant = "standard"
$DataFile = "data/raw/tai256c.dat"
$OutputDir = "results/standard_ga/"
$Population = 100
$Generations = 500
$CrossoverRate = 0.8
$MutationRate = 0.02
$Elitismo = $true
$Seed = 42  # Especifica una semilla fija o cámbiala a $null para una semilla aleatoria

# Crear el directorio de salida si no existe
New-Item -ItemType Directory -Path $OutputDir -Force

# Activar entorno virtual
try {
    & "venv\Scripts\Activate.ps1" -ErrorAction Stop
} catch {
    Handle-Error "No se pudo activar el entorno virtual."
}

Write-Host "===== Inicio del Algoritmo Genético Estándar ====="

# Ejecutar el script principal con los parámetros adecuados
try {
    if ($Seed -ne $null) {
        python src/main.py `
            --variant $Variant `
            --data $DataFile `
            --output $OutputDir `
            --population $Population `
            --generations $Generations `
            --crossover_rate $CrossoverRate `
            --mutation_rate $MutationRate `
            --elitismo `
            --seed $Seed
    }
    else {
        python src/main.py `
            --variant $Variant `
            --data $DataFile `
            --output $OutputDir `
            --population $Population `
            --generations $Generations `
            --crossover_rate $CrossoverRate `
            --mutation_rate $MutationRate `
            --elitismo
    }
} catch {
    Handle-Error "Algoritmo Genético Estándar falló."
}

Write-Host "===== Fin del Algoritmo Genético Estándar ====="
Write-Host "Resultados guardados en $OutputDir"

# Desactivar entorno virtual
deactivate