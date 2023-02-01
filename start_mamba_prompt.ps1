$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
powershell -NoExit -NoProfile -f (Join-Path -Path $scriptPath -ChildPath "mamba\profile.ps1")