# Pit Lane: script de status line que guarda el uso del plan para el freno de gasto (R-30).
# Lee el JSON de la status line por la entrada estándar y escribe ~/.claude/pit-lane-uso.json.
# No falla si faltan los campos rate_limits (por ejemplo, antes de la primera respuesta de la API).
param(
    [string]$Ruta = (Join-Path $HOME '.claude/pit-lane-uso.json')
)

$cinco = $null
$siete = $null
try {
    $datos = $input | Out-String | ConvertFrom-Json
    if ($datos.rate_limits.five_hour) { $cinco = $datos.rate_limits.five_hour.used_percentage }
    if ($datos.rate_limits.seven_day) { $siete = $datos.rate_limits.seven_day.used_percentage }
} catch {
    # Entrada vacía o JSON inválido: se imprime la línea con guiones y no se escribe nada.
}

if ($null -ne $cinco -or $null -ne $siete) {
    try {
        $json = [ordered]@{
            five_hour_used_percentage = $cinco
            seven_day_used_percentage = $siete
            actualizado               = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
        } | ConvertTo-Json
        # UTF-8 sin BOM: Windows PowerShell 5.1 añade BOM con -Encoding utf8.
        [System.IO.File]::WriteAllText($Ruta, $json, (New-Object System.Text.UTF8Encoding($false)))
    } catch {
        # Un fallo al escribir nunca debe romper la status line.
    }
}

$t5 = if ($null -ne $cinco) { "$([math]::Round([double]$cinco))%" } else { '--' }
$t7 = if ($null -ne $siete) { "$([math]::Round([double]$siete))%" } else { '--' }
Write-Host "5h: $t5 | 7d: $t7"
