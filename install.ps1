$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
Write-Output "Installing..."

if (Get-Command tarff -errorAction SilentlyContinue)
{
    Write-Output "Downloading Micromamba..."
    Invoke-Webrequest -URI https://micro.mamba.pm/api/micromamba/win-64/latest -OutFile micromamba.tar.bz2

    Write-Output "Extracting..."
    tar xf micromamba.tar.bz2

    Write-Output "Cleaning up..."
    Remove-Item micromamba.tar.bz2
} else {
    Write-Output "Downloading Micromamba..."
    (New-Object Net.WebClient).DownloadFile('https://murch.physics.wustl.edu/remote/archive/micromamba.zip', 'micromamba.zip')

    Write-Output "Extracting..."
    Expand-Archive micromamba.zip -DestinationPath .

    Write-Output "Cleaning up..."
    Remove-Item micromamba.zip
}

Move-Item -Force Library\bin\micromamba.exe micromamba.exe
Remove-Item -Recurse -Force Library
Remove-Item -Recurse -Force info

Write-Output "Installing base environment..."

$Env:MAMBA_ROOT_PREFIX = $scriptPath
$Env:MAMBA_EXE = (Join-Path -Path $scriptPath -ChildPath "micromamba.exe")
(& $Env:MAMBA_EXE 'shell' 'hook' -s 'powershell' -p $Env:MAMBA_ROOT_PREFIX) | Out-String | Invoke-Expression

micromamba -r "$scriptPath" create -y -n mambabase python=3.8
Start-Sleep 60