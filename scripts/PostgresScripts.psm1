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

function Get-PostgresBinary {
    <#
     # This function will attempt to find the postgres binaries directory and pg_ctl.exe
     # It will first look in the base directory for a folder named pgsql (this is the portable binaries folder).
     # If it does not find it, it will attempt to find one in PATH.
     # If that fails, it will prompt the user to select their PostgreSQL binaries folder.
     #>
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$true)]
        [String] $BaseDir,

        [Parameter(Mandatory=$true)]
        [String] $Binary
    )

    $LocalPgsqlBinary = Join-Path $BaseDir "pgsql" "bin" $Binary

    If (-not (Test-Path $LocalPgsqlBinary -PathType Leaf)) {
        # Check for pg_ctl in path first
        If (Get-Command $Binary -ErrorAction SilentlyContinue) {
            $PgCtl = Get-Command $Binary
            $PgCtl.Source
        } Else {
            # If pg_ctl could not be found, prompt the user to select their binaries folder.
            Write-Host -ForegroundColor Red "It seems you don't have PostgreSQL binaries downloaded locally."
            Write-Host "This script expected $Binary to be in `"$LocalPgsqlBinary`", which you can get from the binaries zip from the official website."

            Write-Host -ForegroundColor Blue "Please pick the folder in which PostgreSQL binaries reside"

            # Load and show the folder picker
            Add-Type -AssemblyName System.Windows.Forms
            $FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
            $FolderBrowser.ShowDialog() | Out-Null

            If ($FolderBrowser.SelectedPath -eq "")
            {
                Write-Host -ForegroundColor Red "No folder selected, exiting."
                exit 1
            }

            Write-Host -ForegroundColor Blue "Selected: `"$( $FolderBrowser.SelectedPath )`""
            Write-Host

            $ChosenPgsqlBinary = Join-Path $FolderBrowser.SelectedPath $Binary
            if (-not(Test-Path $ChosenPgsqlBinary -PathType Leaf))
            {
                Write-Host -ForegroundColor Red "The chosen folder does not contain $Binary, exiting."
                exit 1
            }

            $ChosenPgsqlBinary
        }
    } Else {
        $LocalPgsqlBinary
    }
}