function Write-Header {
    <#
     # This function will print the script header colourfully,
     # complete with a title and description.
     #>
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$true)]
        [String] $Title,

        [Parameter(Mandatory=$false)]
        [String] $Description = ""
    )

    Write-Host -ForegroundColor DarkYellow "=="
    Write-Host -ForegroundColor DarkYellow "== $Title"
    If (-not ($Description -eq "")) {
        Write-Host -ForegroundColor DarkYellow "== $Description"
    }
    Write-Host -ForegroundColor DarkYellow "=="
    Write-Host
}

function Write-ScriptLine {
    <#
     # This function will color a log entry with the format "[log title] log content".
     # Square brackets will be blue, the log name cyan and the content white.
     #
     #>
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$true)]
        [String] $Name,

        [Parameter(Mandatory=$true)]
        [String] $Content
    )

    Write-Host -ForegroundColor Blue "[" -NoNewline
    Write-Host -ForegroundColor Cyan "$Name" -NoNewline
    Write-Host -ForegroundColor Blue "] " -NoNewline
    Write-Host "$Content"
}

function Get-PostgresBinaryDir {
    <#
     # This function will attempt to find the postgres binaries directory.
     # It will first look in the base directory for a folder named pgsql (this is the portable binaries folder).
     # If it does not find it, it will prompt the user to select their PostgreSQL binaries folder.
     #>
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$true)]
        [String] $BaseDir
    )

    $LocalPgsql = Join-Path $BaseDir "pgsql"
    $LocalPgsqlBin = Join-Path $LocalPgsql "bin"

    If (-not (Test-Path $LocalPgsqlBin -PathType Container)) {
        Write-Host -ForegroundColor Red "It seems you don't have PostgreSQL binaries downloaded locally."
        Write-Host "This script expected binaries to be in `"$LocalPgsqlBin`", which is the portable binary zip you can get from the official website."

        Write-Host -ForegroundColor Blue "Please pick the folder in which PostgreSQL binaries reside (initdb/psql/...)."

        # Load and show the folder picker
        Add-Type -AssemblyName System.Windows.Forms
        $FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
        $FolderBrowser.ShowDialog() | Out-Null

        If ($FolderBrowser.SelectedPath -eq "") {
            Write-Host -ForegroundColor Red "No folder selected, exiting."
            exit 1
        }

        Write-Host -ForegroundColor Blue "Selected: `"$($FolderBrowser.SelectedPath)`""
        Write-Host

        $FolderBrowser.SelectedPath
    } Else {
        $LocalPgsqlBin
    }
}