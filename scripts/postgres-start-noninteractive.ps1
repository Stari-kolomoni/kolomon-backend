Import-Module "$PSScriptRoot\PostgresScripts.psm1"
Write-Header -Title "PostgreSQL Run Script"

$BaseDir = Join-Path $PSScriptRoot ".." -Resolve
$DatabaseDir = Join-Path $BaseDir "database"
$LogFile = Join-Path $BaseDir "db.log"

$PostgresBinary = Get-PostgresBinary -BaseDir $BaseDir -Binary "pg_ctl.exe"
Write-ScriptLine -Name "Script" -Content "Using binary: `"$PostgresBinary`""


If (-not (Test-Path $DatabaseDir -PathType Container)) {
    Write-Host -ForegroundColor Red "It seems like there is no database at `"$DatabaseDir`""
    Write-Host -ForegroundColor Red "You might want to set up the database there first using the postgres-init.ps1 script."
    exit 1
}

Write-ScriptLine -Name "Script" -Content "Starting PostgreSQL in background (using pg_ctl start)"
Invoke-Expression "$PostgresBinary start -D $DatabaseDir -l $LogFile"
Write-ScriptLine -Name "Script" -Content "PostgreSQL started, press Ctrl+C to gracefully stop the server."

try {
    while($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-ScriptLine -Name "Script" -Content "Stopping PostgreSQL."
    Invoke-Expression "$PostgresBinary stop -D $DatabaseDir -m smart"
}
