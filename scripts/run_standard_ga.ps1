# scripts/run_standard_ga.ps1

# Descripción:
# Ejecuta el Algoritmo Genético Estándar para el QAP utilizando el archivo de datos tai256c.dat.
# Los resultados se guardarán en el directorio results/standard_ga/

# Función para manejar errores
function Handle-Error {
    param([string]$message)
    Write-Error $message
    exit 1
}

# Definir variables
$Variant = "standard"
$DataFile = "data/raw/tai256c.dat"
$OutputDir = "results/standard_ga/"

# Crear el directorio de salida si no existe
New-Item -ItemType Directory -Path $OutputDir -Force

# Activar entorno virtual
& "venv\Scripts\Activate.ps1" -ErrorAction Stop || Handle-Error "No se pudo activar el entorno virtual."

Write-Host "===== Inicio del Algoritmo Genético Estándar ====="

# Ejecutar el script principal con los parámetros adecuados
python src/main.py --variant $Variant `
                   --data $DataFile `
                   --output $OutputDir *>&1 | Out-File "$OutputDir\ejecucion.log" -Encoding utf8
if ($LASTEXITCODE -ne 0) {
    Handle-Error "Algoritmo Genético Estándar falló."
}

Write-Host "===== Fin del Algoritmo Genético Estándar ====="
Write-Host "Resultados guardados en $OutputDir"

# Desactivar entorno virtual
deactivate