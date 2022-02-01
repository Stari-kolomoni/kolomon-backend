Import-Module "$PSScriptRoot\PostgresScripts.psm1"
Write-Header -Title "PostgreSQL start script"

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

[Console]::TreatControlCAsInput = $true
While ($true) {
    If ([Console]::KeyAvailable) {
        $PressedKey = [System.Console]::readkey($true)
        if (($PressedKey.Modifiers -band [ConsoleModifiers] "control") -and ($PressedKey.Key -eq "C")) {
            # User pressed Ctrl+C, let's gracefully exit
            Write-ScriptLine -Name "Script" -Content "Received Ctrl+C, shutting down..."
            Invoke-Expression "$PostgresBinary stop -D $DatabaseDir -m smart"
            Write-ScriptLine -Name "Script" -Content "PostgreSQL server shut down"
            exit 0
        }
    }
}
