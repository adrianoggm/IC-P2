# scripts/run_all.ps1

# Descripción:
# Ejecuta todas las variantes del Algoritmo Genético secuencialmente.
# Incluye pasos de formateo y verificación de estilo de código antes de la ejecución.

function Handle-Error {
    param([string]$message)
    Write-Error $message
    exit 1
}

# Definir variables
$Variants = @("standard", "baldwinian", "lamarckian")
$DataFile = "data/raw/tai256c.dat"
$Population = 100
$Generations = 500
$CrossoverRate = 0.8
$MutationRate = 0.02
$Elitismo = $true

# Crear directorios de resultados si no existen
foreach ($variant in $Variants) {
    New-Item -ItemType Directory -Path "results/$variant`_ga/" -Force
}

# Activar entorno virtual
try {
    & "venv\Scripts\Activate.ps1" -ErrorAction Stop
} catch {
    Handle-Error "No se pudo activar el entorno virtual."
}

# Formatear código con Black e isort
Write-Host "Formateando código con Black..."
try {
    black src/ tests/ notebooks/
} catch {
    Handle-Error "Formateo con Black falló."
}

Write-Host "Ordenando importaciones con isort..."
try {
    isort src/ tests/
} catch {
    Handle-Error "Ordenación de importaciones con isort falló."
}

# Verificar estilo de código con Flake8
Write-Host "Verificando estilo de código con Flake8..."
try {
    flake8 src/ tests/
} catch {
    Handle-Error "Verificación de estilo con Flake8 falló."
}

# Ejecutar todas las variantes
foreach ($variant in $Variants) {
    Write-Host "Ejecutando Variante $variant del Algoritmo Genético..."
    try {
        & ".\scripts\run_${variant}_ga.ps1"
    } catch {
        Handle-Error "Ejecución de la Variante $variant falló."
    }
}

Write-Host "===== Todas las variantes del Algoritmo Genético han sido ejecutadas correctamente ====="

# Desactivar entorno virtual
deactivate
