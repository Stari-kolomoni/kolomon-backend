Import-Module "$PSScriptRoot\PostgresScripts.psm1"
Write-Header -Title "PostgreSQL stop script"

$BaseDir = Join-Path $PSScriptRoot ".." -Resolve
$DatabaseDir = Join-Path $BaseDir "database"
$PostgresPgctlBinary = Get-PostgresPgctlBinary -BaseDir $BaseDir

If (-not (Test-Path $DatabaseDir -PathType Container)) {
    Write-Host -ForegroundColor Red "It seems like there is no database at `"$DatabaseDir`""
    Write-Host -ForegroundColor Red "You might want to set up the database there first using the postgres-init.ps1 script."
    exit 1
}

Write-ScriptLine -Name "Script" -Content "Stopping PostgreSQL (using pg_ctl stop)"
Invoke-Expression "$PostgresPgctlBinary stop -D $DatabaseDir"
Write-ScriptLine -Name "Script" -Content "PostgreSQL server stopped"
