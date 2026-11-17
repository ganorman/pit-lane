# Puente con Microsoft Office para verificar_office.py (solo Windows con Office instalado).
#   -Accion pdf         exporta un DOCX, PPTX o XLSX a PDF e imprime "PAGINAS=<n>"
#   -Accion recalcular  abre un XLSX en Excel, recalcula todo (CalculateFull) y lo guarda
# Usa siempre una copia: "recalcular" sobrescribe el archivo que recibe.
param(
    [Parameter(Mandatory = $true)][ValidateSet('pdf', 'recalcular')][string]$Accion,
    [Parameter(Mandatory = $true)][string]$Entrada,
    [string]$Salida
)
$ErrorActionPreference = 'Stop'
$Entrada = (Resolve-Path -LiteralPath $Entrada).Path
$ext = [IO.Path]::GetExtension($Entrada).ToLower()
if ($Accion -eq 'pdf') {
    if (-not $Salida) { [Console]::Error.WriteLine('Falta -Salida'); exit 2 }
    $Salida = [IO.Path]::GetFullPath($Salida)
}
$app = $null; $doc = $null
try {
    switch ($ext) {
        { $_ -in '.docx', '.doc' } {
            if ($Accion -ne 'pdf') { throw "recalcular solo aplica a XLSX" }
            $app = New-Object -ComObject Word.Application
            $app.Visible = $false; $app.DisplayAlerts = 0
            $doc = $app.Documents.Open($Entrada, $false, $true)   # sin conversión, solo lectura
            $doc.ExportAsFixedFormat($Salida, 17)                   # 17 = PDF
            "PAGINAS=$($doc.ComputeStatistics(2))"                   # 2 = páginas
            $doc.Close(0)
        }
        { $_ -in '.pptx', '.ppt' } {
            if ($Accion -ne 'pdf') { throw "recalcular solo aplica a XLSX" }
            $app = New-Object -ComObject PowerPoint.Application
            $doc = $app.Presentations.Open($Entrada, -1, 0, 0)       # solo lectura, sin ventana
            $doc.SaveAs($Salida, 32)                                 # 32 = PDF
            "PAGINAS=$($doc.Slides.Count)"
            $doc.Close()
        }
        { $_ -in '.xlsx', '.xlsm', '.xls' } {
            $app = New-Object -ComObject Excel.Application
            $app.Visible = $false; $app.DisplayAlerts = $false
            if ($Accion -eq 'pdf') {
                $doc = $app.Workbooks.Open($Entrada, 0, $true)
                $doc.ExportAsFixedFormat(0, $Salida)                 # 0 = PDF
                "PAGINAS=?"
                $doc.Close($false)
            } else {
                $doc = $app.Workbooks.Open($Entrada, 0, $false)
                $app.CalculateFull()
                $doc.Save()
                "RECALCULADO"
                $doc.Close($false)
            }
        }
        default { throw "Tipo $ext no soportado por Office" }
    }
} catch {
    [Console]::Error.WriteLine("Office: $($_.Exception.Message)")
    exit 1
} finally {
    if ($app) { try { $app.Quit() } catch {} ; [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app) }
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
