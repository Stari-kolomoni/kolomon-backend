Import-Module "$PSScriptRoot\PostgresScripts.psm1"
Write-Header -Title "PostgreSQL database init script"

$BaseDir = Join-Path $PSScriptRoot ".." -Resolve
$DatabaseDir = Join-Path $BaseDir "database"
Write-ScriptLine -Name "Script" -Content "Database dir will be: $DatabaseDir"

$PostgresBinary = Get-PostgresBinary -BaseDir $BaseDir -Binary "pg_ctl.exe"
Write-ScriptLine -Name "Script" -Content "Using binary: `"$PostgresBinary`""


If (Test-Path $DatabaseDir -PathType Container) {
    Write-Host -ForegroundColor Red "The database folder already exists ($DatabaseDir), so this script will exit."
    Write-Host -ForegroundColor Red "If you stil wish to initialize a new database, delete the database folder first."
    exit 1
}

Write-ScriptLine -Name "Script" -Content "Initializing PostgreSQL database (using pg_ctl init)"
Invoke-Expression "$PostgresBinary init -D $DatabaseDir"
Write-ScriptLine -Name "Script" -Content "PostgreSQL database initialized"
Write-ScriptLine -Name "Script" -Content "To run the database, use the postgres-start.ps1 script"
