#region mamba initialize
$Env:MAMBA_ROOT_PREFIX = (Split-Path $MyInvocation.MyCommand.Path -Parent)
$Env:MAMBA_EXE = (Join-Path -Path $Env:MAMBA_ROOT_PREFIX -ChildPath "micromamba.exe")
(& $Env:MAMBA_EXE 'shell' 'hook' -s 'powershell' -p $Env:MAMBA_ROOT_PREFIX) | Out-String | Invoke-Expression
Set-Alias mamba micromamba
Set-Alias conda micromamba
micromamba activate mambabase
#endregion
