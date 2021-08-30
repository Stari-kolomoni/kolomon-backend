Import-Module "$PSScriptRoot\PostgresScripts.psm1"
Write-Header -Title "PostgreSQL start script"

$BaseDir = Join-Path $PSScriptRoot ".." -Resolve
$DatabaseDir = Join-Path $BaseDir "database"
$PostgresPgctlBinary = Get-PostgresPgctlBinary -BaseDir $BaseDir

If (-not (Test-Path $DatabaseDir -PathType Container)) {
    Write-Host -ForegroundColor Red "It seems like there is no database at `"$DatabaseDir`""
    Write-Host -ForegroundColor Red "You might want to set up the database there first using the postgres-init.ps1 script."
    exit 1
}

Write-ScriptLine -Name "Script" -Content "Starting PostgreSQL in background (using pg_ctl start)"
Invoke-Expression "$PostgresPgctlBinary start -D $DatabaseDir -l db.log"
Write-ScriptLine -Name "Script" -Content "PostgreSQL started."
