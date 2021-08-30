Import-Module "$PSScriptRoot\PostgresScripts.psm1"
Write-Header -Title "PostgreSQL database init script"

$BaseDir = Join-Path $PSScriptRoot ".." -Resolve
$LogFile = Join-Path $BaseDir "db.log"
$DatabaseDir = Join-Path $BaseDir "database"
Write-ScriptLine -Name "Script" -Content "Database dir will be: $DatabaseDir"

$PostgresBinary = Get-PostgresBinary -BaseDir $BaseDir -Binary "pg_ctl.exe"
$PostgresBinaryPsql = Get-PostgresBinary -BaseDir $BaseDir -Binary "psql.exe"
Write-ScriptLine -Name "Script" -Content "Using binary: `"$PostgresBinary`""


If (Test-Path $DatabaseDir -PathType Container) {
    Write-Host -ForegroundColor Red "The database folder already exists ($DatabaseDir), so this script will exit."
    Write-Host -ForegroundColor Red "If you stil wish to initialize a new database, delete the database folder first."
    exit 1
}

Write-ScriptLine -Name "Script" -Content "Initializing PostgreSQL database (using pg_ctl init)"
Write-ScriptLine -Name "Script" -Content "The superuser account will have the username `"postgres`"."
Write-ScriptLine -Name "Script" -Content "Note: remember the superuser password you're about to set! You will be asked to provide it later in the script."
Write-ScriptLine -Name "Script" -Content "Warning: using --auth=trust, do not use this in production!"
Invoke-Expression "$PostgresBinary initdb -D $DatabaseDir -o `"--encoding UTF8 --auth=trust --username=postgres --pwprompt`""

Write-ScriptLine -Name "Script" -Content "Temporarily starting server to set up roles"
Invoke-Expression "$PostgresBinary start -D $DatabaseDir -l $LogFile"

Write-ScriptLine -Name "Script" -Content "Creating user kolomon and database kolomondb"
Invoke-Expression "$PostgresBinaryPsql -h localhost -U postgres -c `"CREATE ROLE kolomon WITH PASSWORD 'kolomon' LOGIN`""
Invoke-Expression "$PostgresBinaryPsql -h localhost -U postgres -c 'CREATE DATABASE kolomondb WITH OWNER kolomon ENCODING UTF8'"

Write-ScriptLine -Name "Script" -Content "Shutting down temporary server"
Invoke-Expression "$PostgresBinary stop -D $DatabaseDir"

Write-ScriptLine -Name "Script" -Content "PostgreSQL database initialization finished"
Write-ScriptLine -Name "Script" -Content "To run the database, use the postgres-start.ps1 script"
