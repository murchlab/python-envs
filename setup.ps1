$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition

Write-Output "Installing..."

if ((Get-Command tar -errorAction SilentlyContinue) -AND (Get-Command bzip2 -errorAction SilentlyContinue))
{
    Write-Output "Downloading Micromamba..."
    Invoke-Webrequest -URI https://micro.mamba.pm/api/micromamba/win-64/latest -OutFile mamba\micromamba.tar.bz2

    Write-Output "Extracting..."
    tar xfC mamba\micromamba.tar.bz2 mamba\

    Write-Output "Cleaning up..."
    Remove-Item mamba\micromamba.tar.bz2
} else {
    Write-Output "Downloading Micromamba..."
    (New-Object Net.WebClient).DownloadFile('https://murch.physics.wustl.edu/remote/archive/micromamba.zip', 'mamba\micromamba.zip')

    Write-Output "Extracting..."
    Expand-Archive mamba\micromamba.zip -DestinationPath mamba\

    Write-Output "Cleaning up..."
    Remove-Item mamba\micromamba.zip
}

Move-Item -Force mamba\Library\bin\micromamba.exe mamba\micromamba.exe
Remove-Item -Recurse -Force mamba\Library\
Remove-Item -Recurse -Force mamba\info\

Write-Output "Installing base environment..."

$Env:MAMBA_ROOT_PREFIX = Join-Path -Path $scriptPath -ChildPath "mamba"
$Env:MAMBA_EXE = Join-Path -Path $Env:MAMBA_ROOT_PREFIX -ChildPath "micromamba.exe"
(& $Env:MAMBA_EXE 'shell' 'hook' -s 'powershell' -p $Env:MAMBA_ROOT_PREFIX) | Out-String | Invoke-Expression

micromamba -r "$Env:MAMBA_ROOT_PREFIX" create -y -n mambabase38 --file mamba\mambabase38.yml
# Start-Sleep 60